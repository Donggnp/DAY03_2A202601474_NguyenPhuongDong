"""
🛠️ TOOL REGISTRY & SCHEMAS (Dành cho Role 2: Tool & Spec Engineer)
Nơi khai báo tất cả các "món đồ nghề" mà ReAct Agent có thể gọi.
"""
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
    
    # Mock data cơ bản
    mapping = {
        "A00": "Toán, Lý, Hóa: Phù hợp với Kỹ thuật, CNTT, Khoa học dữ liệu, Cơ điện tử, Logistics.",
        "A01": "Toán, Lý, Anh: Phù hợp với CNTT, Kinh tế, Quản trị kinh doanh, Marketing, Khoa học máy tính.",
        "B00": "Toán, Hóa, Sinh: Phù hợp với Y dược, Công nghệ sinh học, Khoa học môi trường, Nông nghiệp.",
        "C00": "Văn, Sử, Địa: Phù hợp với Báo chí, Luật, Sư phạm, Du lịch, Tâm lý học.",
        "D01": "Toán, Văn, Anh: Phù hợp với Ngôn ngữ, Kinh tế, Truyền thông, Quan hệ quốc tế, Quản trị nhân sự."
    }
    
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
    
    # Mock data cho một số ngành
    careers = {
        "công nghệ thông tin": {
            "mo_ta": "Lập trình, thiết kế, phát triển và bảo trì phần mềm, hệ thống mạng.",
            "ky_nang": "Tư duy logic, học hỏi nhanh, tiếng Anh tốt, kiên trì.",
            "muc_luong": "Mới ra trường: 10-15 triệu/tháng. Kinh nghiệm 3-5 năm: 25-50 triệu/tháng.",
            "trien_vong": "Rất cao trong 5-10 năm tới."
        },
        "marketing": {
            "mo_ta": "Nghiên cứu thị trường, xây dựng chiến lược quảng cáo, PR, quản lý thương hiệu.",
            "ky_nang": "Sáng tạo, giao tiếp tốt, nhạy bén với xu hướng, phân tích dữ liệu.",
            "muc_luong": "Mới ra trường: 8-12 triệu/tháng. Quản lý: 20-40 triệu/tháng.",
            "trien_vong": "Nhu cầu luôn cao ở mọi lĩnh vực kinh doanh."
        },
        "logistics": {
            "mo_ta": "Quản lý chuỗi cung ứng, vận tải, kho bãi, xuất nhập khẩu.",
            "ky_nang": "Lập kế hoạch, giải quyết vấn đề, giao tiếp ngoại ngữ, cẩn thận.",
            "muc_luong": "Mới ra trường: 9-14 triệu/tháng. Trưởng phòng: 25-45 triệu/tháng.",
            "trien_vong": "Ngành công nghiệp đang bùng nổ nhờ thương mại điện tử."
        }
    }
    
    for key, info in careers.items():
        if key in career_name_lower or career_name_lower in key:
            return (
                f"Thông tin nghề: {key.upper()}\n"
                f"- Mô tả: {info['mo_ta']}\n"
                f"- Kỹ năng cần có: {info['ky_nang']}\n"
                f"- Mức lương tham khảo: {info['muc_luong']}\n"
                f"- Triển vọng: {info['trien_vong']}"
            )
            
    return f"Chưa tìm thấy dữ liệu chi tiết cho ngành '{career_name}'. Bạn thử các ngành như: Công nghệ thông tin, Marketing, Logistics..."


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
    # Mock data trường học
    universities = [
        {"name": "Đại học Bách Khoa Hà Nội", "region": "Miền Bắc", "majors": ["CNTT", "Kỹ thuật", "Cơ điện tử"], "tuition_year": 30000000},
        {"name": "Đại học Kinh tế Quốc dân", "region": "Miền Bắc", "majors": ["Kinh tế", "Marketing", "Kế toán"], "tuition_year": 25000000},
        {"name": "Đại học FPT", "region": "Toàn quốc", "majors": ["CNTT", "Marketing", "Ngôn ngữ"], "tuition_year": 90000000},
        {"name": "Đại học Khoa học Tự nhiên TP.HCM", "region": "Miền Nam", "majors": ["CNTT", "Khoa học dữ liệu", "Sinh học"], "tuition_year": 28000000},
        {"name": "RMIT Việt Nam", "region": "Toàn quốc", "majors": ["Kinh tế", "Truyền thông", "IT", "Marketing"], "tuition_year": 320000000},
    ]
    
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


def personality_assessment(answers: str) -> str:
    """
    Đánh giá tính cách (RIASEC/MBTI/Big Five) từ câu trả lời của người dùng.
    Args:
        answers (str): Các câu trả lời của người dùng về sở thích, thói quen.
    Returns:
        str: Kết quả đánh giá nhóm tính cách.
    """
    ans_lower = answers.lower()
    if "kỹ thuật" in ans_lower or "máy móc" in ans_lower or "sửa chữa" in ans_lower:
        return "Kết quả RIASEC: Nhóm R (Realistic - Thực tế). Phù hợp: Kỹ sư, CNTT, Cơ khí."
    elif "nghệ thuật" in ans_lower or "sáng tạo" in ans_lower or "vẽ" in ans_lower:
        return "Kết quả RIASEC: Nhóm A (Artistic - Nghệ thuật). Phù hợp: Thiết kế, Truyền thông, Marketing."
    elif "giao tiếp" in ans_lower or "giúp đỡ" in ans_lower or "con người" in ans_lower:
        return "Kết quả RIASEC: Nhóm S (Social - Xã hội). Phù hợp: Giáo viên, Tâm lý học, Nhân sự."
    else:
        return "Kết quả RIASEC: Đang phân tích. Vui lòng cung cấp thêm thông tin về sở thích lúc rảnh rỗi của bạn."


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
    "personality_assessment": personality_assessment,
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
