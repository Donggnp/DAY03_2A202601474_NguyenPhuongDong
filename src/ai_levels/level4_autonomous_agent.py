"""
🚀 CẤP ĐỘ 4: AUTONOMOUS AGENT (Agent Tự Chủ với Planning, Memory & OpenAI Tools)
Tự chia nhỏ mục tiêu phức tạp thành nhiều bước, duy trì bộ nhớ (Memory), gọi Tool và tự đánh giá tiến độ.
"""

import json
import re
import sys
import os

# Thêm thư mục src vào sys.path để import các module tools, providers, level3
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools import AVAILABLE_TOOLS
from providers import OpenAIProvider, get_llm_provider
from ai_levels.level3_reactive_agent import parse_action, execute_tool

AUTONOMOUS_SYSTEM_PROMPT = """Bạn là một Autonomous Goal Agent - Trợ lý AI Tự Chủ Cao Cấp về Định Hướng Học Tập và Sự Nghiệp.
Nhiệm vụ của bạn là tiếp nhận một MỤC TIÊU LỚN (Goal) từ người dùng, tự động lập kế hoạch (Planning), gọi các Công Cụ (Tools) cần thiết, duy trì Bộ Nhớ (Memory), và tổng hợp thành báo cáo hướng nghiệp hoàn chỉnh.

🛠️ CÁC CÔNG CỤ (TOOLS) KHẢ DỤNG TRONG HỆ THỐNG:
1. major_matching(subject_group: str) - Tra cứu nhóm ngành theo khối thi (A00, A01, B00, C00, D01...).
2. career_database_search(career_name: str) - Tra cứu mô tả, kỹ năng, mức lương và triển vọng nghề nghiệp.
3. university_search(major: str, region: str = "Toàn quốc", max_tuition: int = 100000000) - Tìm trường đại học theo ngành, khu vực (Miền Bắc/Miền Nam/Toàn quốc) và học phí tối đa (VNĐ).
4. get_personality_questions(section: str = "riasec", limit: int = 5) - Lấy câu hỏi trắc nghiệm tính cách.
5. calculate_personality_score(answers_json: str) - Tính điểm RIASEC/MBTI từ câu trả lời.

📋 ĐỊNH DẠNG PHẢN HỒI BẮT BUỘC TRONG MỖI BƯỚC:

Nếu cần gọi công cụ để thực hiện bước hiện tại:
Plan: [Mô tả ngắn gọn kế hoạch của bước này]
Action: tên_công_cụ(tham_số)

Nếu đã có đủ dữ liệu và HOÀN THÀNH MỤC TIÊU:
Plan: Đã hoàn thành tất cả các bước.
Action: COMPLETE
Final Answer: [Báo cáo tổng hợp chi tiết, mạch lạc, phân tích chiều sâu để giải quyết hoàn toàn mục tiêu của người dùng]
"""

class AutonomousGoalAgent:
    def __init__(self, goal: str, max_steps: int = 5, provider=None):
        self.goal = goal
        self.max_steps = max_steps
        self.provider = provider or OpenAIProvider()
        if isinstance(self.provider, str):
            self.provider = get_llm_provider(self.provider)
        self.memory = []  # Bộ nhớ lưu vết các bước đã thực hiện
        self.final_summary = ""

    def execute(self, verbose: bool = True) -> dict:
        """
        Thực thi vòng lặp tự chủ Planning - Execution - Memory Evaluation.
        """
        if verbose:
            print(f"\n🚀 === BẮT ĐẦU AUTONOMOUS GOAL AGENT (OPENAI) ===")
            print(f"🎯 Goal: {self.goal}")
            print(f"🤖 Provider: {self.provider.__class__.__name__}\n")

        history_context = [f"MỤC TIÊU CẦN ĐẠT ĐƯỢC: {self.goal}"]

        for step in range(1, self.max_steps + 1):
            if verbose:
                print(f"--- 🔄 Vòng lặp Tự Chủ Step {step}/{self.max_steps} ---")

            prompt = "\n\n".join(history_context)
            if verbose:
                print("🧠 LLM đang lập kế hoạch & quyết định hành động...")

            response = self.provider.generate(prompt, system_prompt=AUTONOMOUS_SYSTEM_PROMPT)

            if verbose:
                print(f"📝 Agent Response:\n{response}\n")

            history_context.append(f"Step {step} Response:\n{response}")

            # Trích xuất Plan
            plan_match = re.search(r'Plan:\s*(.*?)(?=\nAction:|\nFinal Answer:|$)', response, re.DOTALL | re.IGNORECASE)
            plan = plan_match.group(1).strip() if plan_match else f"Thực hiện bước {step}"

            # Check xem đã có Final Answer chưa
            if "Final Answer:" in response:
                self.final_summary = response.split("Final Answer:")[-1].strip()
                self.memory.append({
                    "step": step,
                    "plan": plan,
                    "action": "COMPLETE",
                    "result": "Đã đạt mục tiêu.",
                    "final_answer": self.final_summary
                })
                if verbose:
                    print(f"🎯 [Goal Evaluation]: Mục tiêu đã hoàn thành ở bước {step}!")
                    print(f"📋 Final Report:\n{self.final_summary}\n")
                break

            # Parse Action
            tool_name, params = parse_action(response)

            if tool_name and tool_name.upper() == "COMPLETE":
                self.final_summary = response
                self.memory.append({
                    "step": step,
                    "plan": plan,
                    "action": "COMPLETE",
                    "result": "Hoàn tất mục tiêu."
                })
                break

            if not tool_name:
                # Nếu không nhận diện được action, tiếp tục với prompt nhắc nhở
                self.memory.append({
                    "step": step,
                    "plan": plan,
                    "action": "N/A",
                    "result": "Không nhận diện được tool, tự suy luận."
                })
                history_context.append("System: Hãy chọn một Action hợp lệ hoặc ghi Action: COMPLETE nếu đã xong.")
                continue

            action_str = f"{tool_name}({', '.join(map(repr, params))})"
            if verbose:
                print(f"🛠️ [Execution]: Call Tool {action_str}")

            tool_result = execute_tool(tool_name, params)

            if verbose:
                print(f"👁️ [Observation]: {tool_result}")
                print(f"💾 [Memory Saved]: Đã ghi nhận bước {step} vào bộ nhớ.\n")

            self.memory.append({
                "step": step,
                "plan": plan,
                "action": action_str,
                "result": tool_result
            })

            history_context.append(f"Step {step} Observation (Kết quả Tool {tool_name}):\n{tool_result}")

        if not self.final_summary and self.memory:
            # Nếu chưa có final_summary chính thức, yêu cầu LLM tổng hợp từ bộ nhớ
            synthesis_prompt = f"Dựa trên MỤC TIÊU: {self.goal} và BỘ NHỚ các bước đã thực hiện bên dưới, hãy đưa ra BÁO CÁO TỔNG HỢP VÀ LỜI KHUYÊN HOÀN CHỈNH:\n" + json.dumps(self.memory, ensure_ascii=False, indent=2)
            self.final_summary = self.provider.generate(synthesis_prompt)

        return {
            "goal": self.goal,
            "memory": self.memory,
            "final_summary": self.final_summary,
            "success": True if self.final_summary else False
        }


if __name__ == "__main__":
    goal = "Lên kế hoạch tư vấn cho học sinh thi khối A00, tìm hiểu ngành Công nghệ thông tin và danh sách trường tại Miền Bắc có học phí dưới 40 triệu."
    agent = AutonomousGoalAgent(goal=goal, max_steps=4)
    res = agent.execute(verbose=True)
    print("\n" + "="*60)
    print("SUMMARY RESULT:")
    print(res["final_summary"])
