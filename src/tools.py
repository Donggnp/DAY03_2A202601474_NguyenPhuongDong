"""
🛠️ TOOL REGISTRY & SCHEMAS (Dành cho Role 2: Tool & Spec Engineer)
Nơi khai báo tất cả các "món đồ nghề" mà ReAct Agent có thể gọi.
"""
import os
import json
from typing import Optional

def major_matching(subject_group: str) -> str:
    """
    Ghép tổ hợp môn học (khối thi) với các nhóm ngành học phù hợp.
    
    Args:
        subject_group (str): Tổ hợp môn/Khối thi (Ví dụ: 'A00', 'A01', 'B00', 'D01')
        
    Returns:
        str: Danh sách các nhóm ngành phù hợp với khối thi đó.
    """
    subject_group = subject_group.strip().upper()
    
    # Read from config
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(os.path.dirname(current_dir), "config", "major_mapping.json")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            mapping = json.load(f)
    except Exception as e:
        return f"Lỗi đọc dữ liệu tổ hợp môn: {e}"
    
    if subject_group in mapping:
        return f"Với tổ hợp {subject_group}, các nhóm ngành gợi ý: {mapping[subject_group]}"
    else:
        return f"Hiện tại hệ thống chưa có dữ liệu chi tiết cho tổ hợp {subject_group}. Hãy thử các khối phổ biến như A00, A01, B00, C00, D01."


def career_database_search(career_name: str) -> str:
    """
    Tra cứu thông tin chi tiết về một ngành nghề (mô tả, kỹ năng, mức lương).
    
    Args:
        career_name (str): Tên ngành nghề (Ví dụ: 'Công nghệ thông tin', 'Marketing', 'Logistics')
        
    Returns:
        str: Thông tin chi tiết về ngành nghề.
    """
    career_name_lower = career_name.lower()
    
    # Read from json file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(os.path.dirname(current_dir), "config", "careers.json")
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            careers = json.load(f)
    except Exception as e:
        return f"Lỗi đọc dữ liệu ngành nghề: {e}"
    
    for key, info in careers.items():
        if key in career_name_lower or career_name_lower in key:
            return (
                f"Thông tin nghề: {key.upper()}\n"
                f"- Mô tả: {info['mo_ta']}\n"
                f"- Kỹ năng cần có: {info['ky_nang']}\n"
                f"- Mức lương tham khảo: {info['muc_luong']}\n"
                f"- Triển vọng: {info['trien_vong']}"
            )
            
    return f"Chưa tìm thấy dữ liệu chi tiết cho ngành '{career_name}'. Bạn thử tìm kiếm theo từ khóa chung hơn."


def university_search(major: str, region: str = "Toàn quốc", max_tuition: int = 100000000) -> str:
    """
    Tìm kiếm trường đại học phù hợp dựa trên ngành học, khu vực và ngân sách học phí.
    
    Args:
        major (str): Ngành học quan tâm (Ví dụ: 'CNTT', 'Kinh tế')
        region (str): Khu vực ('Miền Bắc', 'Miền Nam', 'Toàn quốc'). Mặc định: 'Toàn quốc'.
        max_tuition (int): Học phí tối đa 1 năm (VNĐ). Mặc định: 100000000 (100 triệu).
        
    Returns:
        str: Danh sách các trường đại học thỏa mãn tiêu chí.
    """
    # Read from config
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(os.path.dirname(current_dir), "config", "universities.json")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            universities = json.load(f)
    except Exception as e:
        return f"Lỗi đọc dữ liệu trường học: {e}"
    
    results = []
    major_lower = major.lower()
    
    for uni in universities:
        # Check ngành
        match_major = any(major_lower in m.lower() or m.lower() in major_lower for m in uni["majors"])
        # Check khu vực
        match_region = (region == "Toàn quốc") or (uni["region"] == "Toàn quốc") or (region.lower() in uni["region"].lower())
        # Check học phí
        match_tuition = uni["tuition_year"] <= max_tuition
        
        if match_major and match_region and match_tuition:
            tuition_mil = int(uni["tuition_year"] / 1000000)
            results.append(f"- {uni['name']} ({uni['region']}) | Học phí: ~{tuition_mil} triệu/năm | Ngành: {', '.join(uni['majors'])}")
            
    if results:
        return f"Kết quả tìm kiếm trường đào tạo nhóm ngành '{major}' (Khu vực: {region}, Học phí < {int(max_tuition/1000000)} triệu/năm):\n" + "\n".join(results)
    else:
        return f"Không tìm thấy trường nào phù hợp với tiêu chí: Ngành '{major}', Khu vực '{region}', Học phí dưới {int(max_tuition/1000000)} triệu/năm."


def get_personality_questions(section: str = "riasec", limit: int = 5) -> str:
    """
    Lấy danh sách các câu hỏi trắc nghiệm tính cách.
    Args:
        section (str): Phần cần lấy ('riasec', 'mbti' hoặc 'all').
        limit (int): Số lượng câu hỏi muốn lấy.
    Returns:
        str: Danh sách câu hỏi (kèm ID).
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(os.path.dirname(current_dir), "config", "question.json")
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return f"Lỗi đọc dữ liệu câu hỏi: {e}"
        
    questions = data.get("questions", [])
    if section != "all":
        questions = [q for q in questions if q.get("section") == section]
        
    questions = questions[:limit]
    
    result = []
    for q in questions:
        result.append(f"[{q['id']}] {q['text']}")
        
    return "Danh sách câu hỏi:\n" + "\n".join(result)


def calculate_personality_score(answers_json: str) -> str:
    """
    Tính điểm trắc nghiệm tính cách dựa trên câu trả lời.
    Args:
        answers_json (str): Chuỗi JSON { "ID_câu_hỏi": điểm_1_đến_5 }. VD: '{"R01": 5, "I01": 3}'
    Returns:
        str: Kết quả phân tích tính cách RIASEC / MBTI.
    """
    try:
        answers = json.loads(answers_json)
    except Exception:
        return "Lỗi: Đầu vào answers_json phải là một chuỗi JSON hợp lệ (VD: {\"R01\": 5, \"I01\": 3})."
        
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(os.path.dirname(current_dir), "config", "question.json")
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return f"Lỗi đọc cấu hình điểm: {e}"
        
    riasec_scores = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}
    mbti_scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
    
    questions = data.get("questions", [])
    q_map = {q["id"]: q for q in questions}
    
    for q_id, score in answers.items():
        if q_id not in q_map:
            continue
        q = q_map[q_id]
        if q["section"] == "riasec":
            trait = q.get("trait")
            if trait in riasec_scores:
                riasec_scores[trait] += int(score)
        elif q["section"] == "mbti":
            pole = q.get("pole")
            if pole in mbti_scores:
                mbti_scores[pole] += int(score)
                
    result_text = []
    
    if sum(riasec_scores.values()) > 0:
        sorted_riasec = sorted(riasec_scores.items(), key=lambda item: item[1], reverse=True)
        top_3 = sorted_riasec[:3]
        holland_code = "".join([t[0] for t in top_3])
        result_text.append(f"Mã Holland (RIASEC) của bạn là: {holland_code}")
        
        dimensions = data.get("dimensions", {}).get("riasec", {})
        for trait, score in top_3:
            name_vi = dimensions.get(trait, {}).get("name_vi", trait)
            result_text.append(f"- {name_vi}: {score} điểm")
            
    if sum(mbti_scores.values()) > 0:
        mbti_result = ""
        mbti_result += "E" if mbti_scores["E"] >= mbti_scores["I"] else "I"
        mbti_result += "S" if mbti_scores["S"] >= mbti_scores["N"] else "N"
        mbti_result += "T" if mbti_scores["T"] >= mbti_scores["F"] else "F"
        mbti_result += "J" if mbti_scores["J"] >= mbti_scores["P"] else "P"
        result_text.append(f"\nNhóm tính cách MBTI của bạn là: {mbti_result}")
        
    if not result_text:
        return "Không có dữ liệu điểm để phân tích. Hãy kiểm tra lại ID câu hỏi."
        
    return "\n".join(result_text)

def academic_strength_analyzer(grades_and_skills: str) -> str:
    """
    Phân tích môn học, kỹ năng, thành tích để tìm điểm mạnh.
    Args:
        grades_and_skills (str): Thông tin điểm số hoặc kỹ năng.
    Returns:
        str: Danh sách điểm mạnh.
    """
    text = grades_and_skills.lower()
    strengths = []
    if "toán" in text or "lý" in text or "logic" in text:
        strengths.append("- Tư duy logic và tính toán số liệu tốt.")
    if "văn" in text or "anh" in text or "giao tiếp" in text:
        strengths.append("- Kỹ năng ngôn ngữ, giao tiếp tốt.")
    if "sinh" in text or "hóa" in text:
        strengths.append("- Khả năng nghiên cứu khoa học tự nhiên.")
        
    if strengths:
        return "Điểm mạnh học tập nổi bật:\n" + "\n".join(strengths)
    return "Chưa rõ điểm mạnh. Vui lòng chia sẻ cụ thể hơn về điểm các môn."


def career_trend_search(industry: str) -> str:
    """
    Tra cứu xu hướng ngành nghề VN.
    Args:
        industry (str): Ngành nghề.
    Returns:
        str: Xu hướng, lương, tăng trưởng.
    """
    ind = industry.lower()
    if "it" in ind or "công nghệ" in ind:
        return "Xu hướng: IT tăng trưởng 15-20%/năm. Nhu cầu AI, Data cao. Lương khởi điểm cao hơn trung bình 30%."
    elif "marketing" in ind:
        return "Xu hướng: Digital Marketing rất hot, cạnh tranh cao. Kỹ năng Data Analytics đang lên ngôi."
    return "Xu hướng: Các ngành Kỹ thuật, Chăm sóc sức khỏe và Dịch vụ đang thiếu hụt nhân lực chất lượng cao."


def financial_filter(budget: int) -> str:
    """
    Lọc trường/ngành theo ngân sách (VNĐ/năm).
    Args:
        budget (int): Ngân sách học phí tối đa / năm (VNĐ).
    Returns:
        str: Tư vấn loại trường.
    """
    budget_mil = budget // 1000000
    if budget_mil <= 20:
        return "Tư vấn tài chính: Nên chọn Đại học công lập truyền thống hoặc Cao đẳng. Cố gắng săn học bổng."
    elif budget_mil <= 50:
        return "Tư vấn tài chính: Phù hợp với nhiều Đại học công lập lớn (Bách Khoa, Kinh tế) ở hệ chuẩn."
    return "Tư vấn tài chính: Phù hợp các chương trình Chất lượng cao, Quốc tế hoặc Tư thục (FPT, RMIT)."


def readiness_assessment(user_input: str) -> str:
    """
    Đánh giá mức độ đã định hướng của người dùng.
    Args:
        user_input (str): Câu trả lời của người dùng.
    Returns:
        str: Beginner / Exploring / Decided.
    """
    text = user_input.lower()
    if "không biết" in text or "mông lung" in text or "chưa nghĩ" in text:
        return "Mức độ: BEGINNER (Chưa định hướng). Cần làm test tính cách."
    elif "phân vân" in text or "chưa chốt" in text:
        return "Mức độ: EXPLORING (Đang khám phá). Cần so sánh chi tiết các ngành."
    return "Mức độ: DECIDED (Đã định hướng). Tập trung tìm trường và lộ trình."


def skill_gap_analysis(current_skills: str, target_career: str) -> str:
    """
    So sánh kỹ năng hiện tại với nghề mong muốn.
    Args:
        current_skills (str): Kỹ năng đang có.
        target_career (str): Nghề mong muốn.
    Returns:
        str: Kỹ năng còn thiếu.
    """
    return f"Phân tích Kỹ năng cho '{target_career}': Nếu bạn đã có '{current_skills}', hãy tập trung cải thiện Ngoại ngữ và Kỹ năng mềm (thuyết trình, làm việc nhóm) - đây là yếu tố thường thiếu."


def learning_path_generator(target_career: str) -> str:
    """
    Đề xuất lộ trình học tập.
    Args:
        target_career (str): Nghề mong muốn.
    Returns:
        str: Lộ trình cơ bản.
    """
    return f"Lộ trình đề xuất cho {target_career}: Năm 1-2 (Xây nền tảng & Tiếng Anh) -> Năm 3 (Thực hành dự án cá nhân/CLB) -> Năm 4 (Thực tập doanh nghiệp)."


def scholarship_search(academic_profile: str) -> str:
    """
    Tra cứu học bổng.
    Args:
        academic_profile (str): Thành tích học tập.
    Returns:
        str: Học bổng gợi ý.
    """
    return "Gợi ý Học bổng: Nếu có IELTS > 6.5 và GPA > 8.0, bạn có cơ hội xin học bổng bán phần ở các trường tư thục hoặc xét tuyển thẳng hệ tiên tiến Đại học công lập."


def recommendation_explainer(recommendation: str) -> str:
    """
    Giải thích vì sao chatbot đề xuất ngành/trường.
    Args:
        recommendation (str): Đề xuất đã đưa ra.
    Returns:
        str: Lý do.
    """
    return f"Lý do gợi ý '{recommendation}': Đề xuất này dựa trên sự phù hợp về tính cách, năng lực học tập của bạn, kết hợp với nhu cầu nhân lực tích cực của thị trường hiện tại."


def conversation_memory(action: str, memory_data: str = "") -> str:
    """
    Lưu hoặc truy xuất lịch sử tư vấn (Mô phỏng).
    Args:
        action (str): 'save' hoặc 'load'.
        memory_data (str): Dữ liệu cần lưu (nếu action='save').
    Returns:
        str: Trạng thái hoặc dữ liệu lịch sử.
    """
    if action == "save":
        return f"Đã lưu thông tin vào bộ nhớ: {memory_data}"
    return "Lịch sử bộ nhớ: Đã ghi nhận các yêu cầu trước đó."


# Danh sách các tool được đăng ký để Agent sử dụng
AVAILABLE_TOOLS = {
    "major_matching": major_matching,
    "career_database_search": career_database_search,
    "university_search": university_search,
    "get_personality_questions": get_personality_questions,
    "calculate_personality_score": calculate_personality_score,
    "academic_strength_analyzer": academic_strength_analyzer,
    "career_trend_search": career_trend_search,
    "financial_filter": financial_filter,
    "readiness_assessment": readiness_assessment,
    "skill_gap_analysis": skill_gap_analysis,
    "learning_path_generator": learning_path_generator,
    "scholarship_search": scholarship_search,
    "recommendation_explainer": recommendation_explainer,
    "conversation_memory": conversation_memory,
}
