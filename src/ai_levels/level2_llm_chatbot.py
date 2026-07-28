"""
🤖 CẤP ĐỘ 2: LLM CHATBOT (Baseline Chatbot sử dụng OpenAI API)
Dùng OpenAI LLM sinh câu trả lời tự nhiên mượt mà.
"""

import os
import sys

# Thêm thư mục src vào sys.path để import được các module providers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from providers import OpenAIProvider, get_llm_provider

CHATBOT_BASELINE_PROMPT = """Bạn là một Chatbot tư vấn hướng nghiệp thông thường (Cấp độ 2 - LLM Chatbot) sử dụng OpenAI.
Hãy trả lời câu hỏi của người dùng một cách thân thiện và lịch sự dựa trên kiến thức chung có sẵn của bạn.
Lưu ý: Bạn KHÔNG có các công cụ (tools) để tra cứu dữ liệu thời gian thực (như tìm kiếm trường đại học, tra cứu bài test RIASEC/MBTI trực tiếp từ DB). 
Nếu người dùng hỏi thông tin đòi hỏi tra cứu dữ liệu thực tế thời gian thực, hãy trả lời bằng kiến thức tổng quan và giải thích lịch sự rằng bạn chưa được tích hợp công cụ tra cứu.
"""

def llm_chatbot(user_input: str, provider=None) -> str:
    """
    Hàm gọi LLM Chatbot cấp độ 2 sử dụng OpenAI Provider.
    """
    if provider is None:
        provider = OpenAIProvider()
        
    response = provider.generate(user_input, system_prompt=CHATBOT_BASELINE_PROMPT)
    return response

if __name__ == "__main__":
    print("=== DEMO CẤP ĐỘ 2: LLM CHATBOT (OPENAI) ===")
    provider = OpenAIProvider()
    print(f"🤖 Provider: {provider.__class__.__name__} (Model: {provider.model_name})")
    q = "Xin chào! Bạn có thể giúp tôi tư vấn chọn ngành học không?"
    print(f"User: {q}")
    print(f"Bot : {llm_chatbot(q, provider=provider)}")
