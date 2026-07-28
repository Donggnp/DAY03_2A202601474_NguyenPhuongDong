"""
🧠 CẤP ĐỘ 3: REACTIVE AGENT (ReAct Agent - Thought -> Action -> Observation)
Agent biết suy nghĩ, tự ra quyết định gọi Tool thực tế và quan sát kết quả để trả lời.
"""

import json
import re
import sys
import os

# Thêm thư mục src vào sys.path để import được
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools import AVAILABLE_TOOLS
from prompts import REACT_SYSTEM_PROMPT, MAX_ITERATIONS
from providers import get_llm_provider


def parse_action(response: str):
    """
    Parse phản hồi của LLM để tìm Action cần thực hiện.
    Format mong đợi: Action: tool_name(param1, param2, ...)
    
    Returns:
        tuple: (tool_name, params) hoặc (None, None) nếu không tìm thấy
    """
    # Tìm dòng Action:
    action_match = re.search(r'Action:\s*(\w+)\((.*?)\)', response, re.IGNORECASE)
    
    if action_match:
        tool_name = action_match.group(1)
        params_str = action_match.group(2)
        
        # Parse params (xử lý cả string có dấu nháy và số)
        params = []
        if params_str.strip():
            # Tách params bằng dấu phẩy (đơn giản hóa)
            for p in params_str.split(','):
                p = p.strip().strip('"').strip("'")
                # Thử convert sang int nếu là số
                try:
                    p = int(p)
                except:
                    pass
                params.append(p)
        
        return tool_name, params
    
    return None, None


def execute_tool(tool_name: str, params: list):
    """
    Thực thi tool với tham số đã cho.
    
    Returns:
        str: Kết quả từ tool hoặc thông báo lỗi
    """
    if tool_name not in AVAILABLE_TOOLS:
        return f"❌ Lỗi: Tool '{tool_name}' không tồn tại. Các tool khả dụng: {', '.join(AVAILABLE_TOOLS.keys())}"
    
    try:
        tool_func = AVAILABLE_TOOLS[tool_name]
        result = tool_func(*params)
        return result
    except TypeError as e:
        return f"❌ Lỗi tham số cho tool '{tool_name}': {str(e)}"
    except Exception as e:
        return f"❌ Lỗi khi thực thi tool '{tool_name}': {str(e)}"


def reactive_agent_loop(user_query: str, provider=None, verbose=True):
    """
    Vòng lặp ReAct Agent chính: Thought -> Action -> Observation
    
    Args:
        user_query: Câu hỏi của người dùng
        provider: LLM provider (nếu None sẽ dùng provider mặc định từ .env)
        verbose: Có hiển thị chi tiết từng bước hay không
    
    Returns:
        str: Câu trả lời cuối cùng
    """
    if provider is None:
        provider = get_llm_provider()
    
    if verbose:
        print(f"\n{'='*80}")
        print(f"🎯 Câu hỏi người dùng: {user_query}")
        print(f"🤖 Provider đang dùng: {provider.__class__.__name__}")
        print(f"{'='*80}\n")
    
    conversation_history = []
    conversation_history.append(f"User Query: {user_query}")
    
    for iteration in range(1, MAX_ITERATIONS + 1):
        if verbose:
            print(f"\n{'─'*80}")
            print(f"🔄 VÒng LẶP {iteration}/{MAX_ITERATIONS}")
            print(f"{'─'*80}")
        
        # Tạo prompt đầy đủ với lịch sử
        full_prompt = "\n\n".join(conversation_history)
        
        # Gọi LLM
        if verbose:
            print(f"\n💬 Đang gọi LLM...")
        
        response = provider.generate(full_prompt, REACT_SYSTEM_PROMPT)
        
        if verbose:
            print(f"\n🤖 Phản hồi LLM:\n{response}")
        
        conversation_history.append(f"Agent Response:\n{response}")
        
        # Kiểm tra xem đã có Final Answer chưa
        if "Final Answer:" in response:
            # Trích xuất Final Answer
            final_answer = response.split("Final Answer:")[-1].strip()
            
            if verbose:
                print(f"\n{'='*80}")
                print(f"✅ ĐÃ CÓ KẾT QUẢ CUỐI CÙNG")
                print(f"{'='*80}")
                print(f"\n📝 Final Answer:\n{final_answer}\n")
            
            return final_answer
        
        # Parse Action
        tool_name, params = parse_action(response)
        
        if tool_name is None:
            if verbose:
                print(f"\n⚠️ Không tìm thấy Action hợp lệ trong phản hồi. Tiếp tục...")
            # Thêm prompt nhắc nhở
            conversation_history.append("System: Bạn cần chỉ định một Action với định dạng: Action: tool_name(params)")
            continue
        
        if verbose:
            print(f"\n🛠️ Thực thi Action: {tool_name}({', '.join(map(str, params))})")
        
        # Thực thi tool
        observation = execute_tool(tool_name, params)
        
        if verbose:
            print(f"\n👁️ Observation (Kết quả từ tool):\n{observation}")
        
        # Thêm observation vào lịch sử
        conversation_history.append(f"Observation: {observation}")
    
    # Nếu đã hết số lần lặp mà chưa có Final Answer
    error_msg = f"⚠️ Đã đạt giới hạn {MAX_ITERATIONS} vòng lặp mà chưa có câu trả lời cuối cùng. Vui lòng thử lại với câu hỏi rõ ràng hơn."
    
    if verbose:
        print(f"\n{'='*80}")
        print(error_msg)
        print(f"{'='*80}\n")
    
    return error_msg


def test_reactive_agent():
    """Test function cho ReAct Agent"""
    print("\n" + "="*80)
    print("🧪 TEST REACTIVE AGENT - TƯ VẤN ĐỊNH HƯỚNG SỰ NGHIỆP")
    print("="*80)
    
    # Test case 1: Hỏi về tổ hợp môn
    test_queries = [
        "Em học khối A00 (Toán, Lý, Hóa), các ngành nào phù hợp với em?",
        "Em muốn biết thông tin về ngành Công nghệ thông tin",
        "Em có ngân sách 50 triệu/năm, muốn học CNTT ở Miền Bắc thì có trường nào phù hợp?",
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n\n{'#'*80}")
        print(f"TEST CASE {i}")
        print(f"{'#'*80}")
        
        result = reactive_agent_loop(query, verbose=True)
        
        print(f"\n📊 KẾT QUẢ TEST CASE {i}:")
        print(f"Câu hỏi: {query}")
        print(f"Trả lời: {result}")
        
        print(f"\n{'─'*80}\n")
        
        # Chỉ test 1 case để không mất thời gian
        break


if __name__ == "__main__":
    # Chạy test
    test_reactive_agent()

