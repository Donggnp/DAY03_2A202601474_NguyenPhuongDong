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
    if isinstance(major, str) and "=" in major:
        major = major.split("=")[-1].strip().strip("'").strip('"')
    if isinstance(region, str) and "=" in region:
        region = region.split("=")[-1].strip().strip("'").strip('"')
    if isinstance(max_tuition, str):
        if "=" in max_tuition:
            max_tuition = max_tuition.split("=")[-1]
        try:
            max_tuition = int(max_tuition.strip().strip("'").strip('"'))
        except ValueError:
            max_tuition = 100000000

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
    if isinstance(section, str) and "=" in section:
        section = section.split("=")[-1].strip().strip("'").strip('"')
    section = str(section).strip().strip("'").strip('"')

    if isinstance(limit, str):
        if "=" in limit:
            limit = limit.split("=")[-1]
        try:
            limit = int(limit.strip().strip("'").strip('"'))
        except ValueError:
            limit = 5
    elif not isinstance(limit, int):
        try:
            limit = int(limit)
        except Exception:
            limit = 5

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

# Danh sách các tool được đăng ký để Agent sử dụng
AVAILABLE_TOOLS = {
    "major_matching": major_matching,
    "career_database_search": career_database_search,
    "university_search": university_search,
    "get_personality_questions": get_personality_questions,
    "calculate_personality_score": calculate_personality_score,
}
