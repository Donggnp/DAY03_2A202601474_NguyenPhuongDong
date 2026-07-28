"""
🧠 CẤP ĐỘ 3: REACTIVE AGENT (ReAct Agent - Thought -> Action -> Observation)
Sử dụng OpenAI LLM & bộ công cụ trong tools.py.
"""

import json
import re
import sys
import os

# Thêm thư mục src vào sys.path để import các module tools, prompts, providers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools import AVAILABLE_TOOLS
from prompts import REACT_SYSTEM_PROMPT, MAX_ITERATIONS
from providers import OpenAIProvider, get_llm_provider


def parse_action(response: str):
    """
    Parse phản hồi của LLM để tìm Action cần thực hiện.
    Format mong đợi: Action: tool_name(param1, param2, ...)
    
    Returns:
        tuple: (tool_name, params) hoặc (None, None) nếu không tìm thấy
    """
    action_match = re.search(r'Action:\s*(\w+)\s*[\(\[]([^\)\]]*)[\)\]]', response, re.IGNORECASE)
    
    if action_match:
        tool_name = action_match.group(1).strip()
        params_str = action_match.group(2).strip()
        
        params = []
        if params_str:
            # Nếu param là một chuỗi JSON (ví dụ trong calculate_personality_score)
            if params_str.startswith("{") and params_str.endswith("}"):
                params = [params_str]
            else:
                import csv
                import io
                items = []
                try:
                    reader = csv.reader(io.StringIO(params_str), skipinitialspace=True)
                    for row in reader:
                        items.extend(row)
                except Exception:
                    items = params_str.split(',')

                for item in items:
                    item = item.strip().strip("'").strip('"')
                    # Nếu LLM truyền dạng key=value (ví dụ section="riasec" hoặc limit=5)
                    if "=" in item and not (item.startswith("{") and item.endswith("}")):
                        item = item.split("=", 1)[1].strip().strip("'").strip('"')
                    
                    try:
                        item = int(item)
                    except ValueError:
                        try:
                            item = float(item)
                        except ValueError:
                            pass
                    params.append(item)
        
        return tool_name, params
    
    return None, None



def execute_tool(tool_name: str, params: list):
    """
    Thực thi tool từ AVAILABLE_TOOLS trong tools.py với tham số đã cho.
    
    Returns:
        str: Kết quả từ tool hoặc thông báo lỗi
    """
    if tool_name not in AVAILABLE_TOOLS:
        return f"❌ Lỗi: Tool '{tool_name}' không tồn tại. Các tool khả dụng: {', '.join(AVAILABLE_TOOLS.keys())}"
    
    try:
        tool_func = AVAILABLE_TOOLS[tool_name]
        result = tool_func(*params)
        return str(result)
    except TypeError as e:
        return f"❌ Lỗi tham số cho tool '{tool_name}': {str(e)}"
    except Exception as e:
        return f"❌ Lỗi khi thực thi tool '{tool_name}': {str(e)}"


def reactive_agent_loop(user_query: str, provider=None, verbose=True, return_details=False):
    """
    Vòng lặp ReAct Agent chính: Thought -> Action -> Observation sử dụng OpenAI
    
    Args:
        user_query: Câu hỏi của người dùng
        provider: LLM provider (Mặc định dùng OpenAIProvider nếu None)
        verbose: Hiển thị log trên console
        return_details: Nếu True, trả về dict chứa {final_answer, steps}
    
    Returns:
        str hoặc dict: Câu trả lời cuối cùng hoặc dict chi tiết các bước ReAct
    """
    if provider is None:
        provider = OpenAIProvider()
    elif isinstance(provider, str):
        provider = get_llm_provider(provider)
    
    if verbose:
        print(f"\n{'='*80}")
        print(f"🎯 [CẤP ĐỘ 3 - REACTIVE AGENT] Câu hỏi: {user_query}")
        print(f"🤖 Provider: {provider.__class__.__name__}")
        print(f"{'='*80}\n")
    
    conversation_history = [f"User Query: {user_query}"]
    steps_log = []
    
    for iteration in range(1, MAX_ITERATIONS + 1):
        full_prompt = "\n\n".join(conversation_history)
        
        if verbose:
            print(f"\n--- 🔄 Vòng lặp ReAct (Step {iteration}/{MAX_ITERATIONS}) ---")
            print(f"💬 Đang gọi OpenAI LLM...")
        
        response = provider.generate(full_prompt, REACT_SYSTEM_PROMPT)
        
        if verbose:
            print(f"🤖 Phản hồi LLM:\n{response}\n")
        
        conversation_history.append(f"Agent Response:\n{response}")
        
        # Parse Thought từ phản hồi
        thought_match = re.search(r'Thought:\s*(.*?)(?=\nAction:|\nFinal Answer:|$)', response, re.DOTALL | re.IGNORECASE)
        thought = thought_match.group(1).strip() if thought_match else response
        
        # Kiểm tra xem đã có Final Answer chưa
        if "Final Answer:" in response:
            final_answer = response.split("Final Answer:")[-1].strip()
            
            steps_log.append({
                "step": iteration,
                "thought": thought,
                "action": "Final Answer",
                "observation": final_answer
            })
            
            if verbose:
                print(f"✅ FINAL ANSWER:\n{final_answer}\n")
            
            if return_details:
                return {
                    "final_answer": final_answer,
                    "steps": steps_log,
                    "success": True
                }
            return final_answer
        
        # Parse Action
        tool_name, params = parse_action(response)
        
        if tool_name is None:
            steps_log.append({
                "step": iteration,
                "thought": thought,
                "action": "None",
                "observation": "Không tìm thấy Action hợp lệ."
            })
            conversation_history.append("System: Bạn cần chỉ định một Action với định dạng: Action: tool_name(params)")
            continue
        
        action_str = f"{tool_name}({', '.join(map(repr, params))})"
        if verbose:
            print(f"🛠️ Thực thi Action: {action_str}")
        
        observation = execute_tool(tool_name, params)
        
        if verbose:
            print(f"👁️ Observation:\n{observation}")
        
        steps_log.append({
            "step": iteration,
            "thought": thought,
            "action": action_str,
            "observation": observation
        })
        
        conversation_history.append(f"Observation: {observation}")
    
    error_msg = f"⚠️ Đã đạt giới hạn {MAX_ITERATIONS} vòng lặp ReAct mà chưa có câu trả lời cuối cùng."
    
    if return_details:
        return {
            "final_answer": error_msg,
            "steps": steps_log,
            "success": False
        }
    return error_msg


if __name__ == "__main__":
    print("=== DEMO CẤP ĐỘ 3: REACTIVE AGENT (OPENAI + TOOLS) ===")
    provider = OpenAIProvider()
    query = "Em học khối A00, tư vấn cho em các ngành phù hợp và thông tin ngành Công nghệ thông tin?"
    res = reactive_agent_loop(query, provider=provider, verbose=True, return_details=True)
    print("\n[RESULT]:")
    print(res["final_answer"])
