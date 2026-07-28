"""
🤖 CẤP ĐỘ 1: RULE-BASED CAREER ADVISOR (Hệ thống Hướng nghiệp dựa trên Luật)
- Input: Bộ câu hỏi trắc nghiệm từ config/question.json (40 câu RIASEC + MBTI rút gọn)
- Output: Đánh giá Nhóm ngành phù hợp, Mã Holland Code, MBTI Type và chi tiết phân tích.
- Giao diện: Tích hợp Giao diện Web tông màu trắng đơn giản, hiện đại (White-themed UI).
"""

import json
import os
import sys
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, List


def load_question_config(config_path: str = None) -> Dict[str, Any]:
    """Tải bộ câu hỏi trắc nghiệm từ config/question.json"""
    if config_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        config_path = os.path.join(base_dir, "config", "question.json")
    
    if not os.path.exists(config_path):
        config_path = "config/question.json"
        
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


class RuleBasedCareerEngine:
    """Động cơ tính toán Rule-Based cho trắc nghiệm RIASEC & MBTI rút gọn"""
    
    SECTOR_RULES = {
        "I": {
            "name": "Công nghệ Thông tin, Khoa học Dữ liệu & Nghiên cứu (R&D)",
            "icon": "💻",
            "description": "Nhóm ngành dành cho những người thích phân tích, khám phá bản chất vấn đề, sử dụng logic và làm việc với dữ liệu/khoa học.",
            "majors": [
                "Khoa học Máy tính / Kỹ thuật Phần mềm",
                "Trí tuệ Nhân tạo (AI) & Khoa học Dữ liệu",
                "An toàn Thông tin & Mạng Máy tính",
                "Công nghệ Sinh học & Dược học Nghiên cứu"
            ],
            "careers": [
                "Lập trình viên / Kỹ sư Phần mềm",
                "Chuyên gia Phân tích Dữ liệu (Data Analyst / Scientist)",
                "Kỹ sư Trí tuệ Nhân tạo (AI Engineer)",
                "Nhà Nghiên cứu Khoa học R&D",
                "Chuyên gia An ninh Mạng"
            ],
            "environment": "Phòng Lab R&D, Công ty Công nghệ, Viện Nghiên cứu, Trung tâm dữ liệu.",
            "work_style": "Độc lập, phân tích logic, tập trung chuyên sâu, ra quyết định dựa trên bằng chứng."
        },
        "R": {
            "name": "Kỹ thuật, Cơ khí, Tự động hóa & Hạ tầng",
            "icon": "⚙️",
            "description": "Nhóm ngành dành cho những người thích làm việc với máy móc, công cụ, thao tác thực tế và môi trường kỹ thuật.",
            "majors": [
                "Kỹ thuật Cơ khí & Chế tạo máy",
                "Kỹ thuật Điện - Điện tử & Tự động hóa",
                "Kỹ thuật Xây dựng & Giao thông",
                "Công nghệ Kỹ thuật Ô tô"
            ],
            "careers": [
                "Kỹ sư Cơ khí / Chế tạo",
                "Kỹ sư Tự động hóa & Robot",
                "Kỹ sư Điện / Điện tử",
                "Kỹ sư Xây dựng & Giám sát Công trình",
                "Chuyên viên Vận hành Máy móc Kỹ thuật"
            ],
            "environment": "Nhà máy sản xuất, Công trường xây dựng, Phòng kỹ thuật vận hành, Trung tâm chế tạo.",
            "work_style": "Thực tế, khéo léo, hành động trực tiếp và tối ưu hóa quy trình kỹ thuật."
        },
        "A": {
            "name": "Thiết kế, Truyền thông Đa phương tiện & Sáng tạo",
            "icon": "🎨",
            "description": "Nhóm ngành dành cho những người giàu trí tưởng tượng, có năng khiếu thẩm mỹ và thích môi trường làm việc linh hoạt.",
            "majors": [
                "Thiết kế Đồ họa (Graphic Design) & UX/UI",
                "Truyền thông Đa phương tiện (Multimedia)",
                "Kiến trúc & Thiết kế Nội thất",
                "Sản xuất Nội dung & Nghệ thuật Biểu diễn"
            ],
            "careers": [
                "Nhà thiết kế UX/UI / Graphic Designer",
                "Giám đốc Sáng tạo (Creative Director)",
                "Chuyên viên Sáng tạo Nội dung (Content Creator)",
                "Kiến trúc sư Nội thất",
                "Biên kịch / Sản xuất Media"
            ],
            "environment": "Agency Truyền thông, Studio Thiết kế, Công ty Game/Film, Làm việc tự do (Freelance).",
            "work_style": "Đổi mới, giàu tưởng tượng, thể hiện cảm xúc và phong cách cá nhân."
        },
        "S": {
            "name": "Giáo dục, Y tế, Tâm lý học & Quản trị Nhân lực",
            "icon": "🤝",
            "description": "Nhóm ngành dành cho những người thích hỗ trợ, giảng dạy, chăm sóc sức khỏe và kết nối cộng đồng.",
            "majors": [
                "Sư phạm & Quản lý Giáo dục",
                "Tâm lý học Ứng dụng & Tư vấn",
                "Y khoa / Điều dưỡng / Y tế Cộng đồng",
                "Quản trị Nhân sự (HRM)"
            ],
            "careers": [
                "Giảng viên / Giáo viên",
                "Chuyên viên Tuyển dụng & Phát triển Nhân lực (HR)",
                "Bác sĩ / Y sĩ / Điều dưỡng",
                "Chuyên viên Tư vấn Tâm lý / Hướng nghiệp",
                "Quản lý Dịch vụ Khách hàng"
            ],
            "environment": "Trường học, Bệnh viện, Bộ phận HR Doanh nghiệp, Trung tâm Tư vấn.",
            "work_style": "Lắng nghe, thấu cảm, kiên nhẫn, tinh thần cộng đồng và chia sẻ."
        },
        "E": {
            "name": "Quản trị Kinh doanh, Marketing & Khởi nghiệp",
            "icon": "📈",
            "description": "Nhóm ngành dành cho những người thích dẫn dắt, thuyết phục, đàm phán và phát triển dự án kinh doanh.",
            "majors": [
                "Quản trị Kinh doanh (MBA/BBA)",
                "Marketing & Digital Marketing",
                "Tài chính - Ngân hàng & Đầu tư",
                "Thương mại Quốc tế & Logistics"
            ],
            "careers": [
                "Giám đốc Kinh doanh (Sales Director / Business Manager)",
                "Quản lý Dự án (Project Manager)",
                "Chuyên viên Marketing / PR Lead",
                "Nhà Khởi nghiệp (Founder / Co-Founder)",
                "Chuyên viên Phân tích Đầu tư"
            ],
            "environment": "Tập đoàn kinh doanh, Startup, Ngân hàng, Công ty Quản lý Quỹ.",
            "work_style": "Quyết đoán, thuyết phục, chấp nhận rủi ro có tính toán và dẫn dắt đội nhóm."
        },
        "C": {
            "name": "Kế toán - Kiểm toán, Tài chính & Hành chính Dữ liệu",
            "icon": "📊",
            "description": "Nhóm ngành dành cho những người cẩn thận, ngăn nắp, thích làm việc với con số và quy trình có hệ thống.",
            "majors": [
                "Kế toán & Kiểm toán",
                "Tài chính Doanh nghiệp",
                "Quản trị Văn phòng & Dữ liệu Hành chính",
                "Quản lý Chuỗi Cung ứng (Logistics & Supply Chain)"
            ],
            "careers": [
                "Chuyên viên Kế toán / Kiểm toán viên",
                "Chuyên viên Quản trị Dữ liệu & Hồ sơ",
                "Chuyên viên Thanh toán & Ngân hàng",
                "Chuyên viên Kiểm soát Chất lượng (QA/QC)",
                "Chuyên viên Logistics & Kho vận"
            ],
            "environment": "Công ty Kiểm toán, Ngân hàng, Phòng Kế toán / Hành chính Doanh nghiệp.",
            "work_style": "Tỉ mỉ, cẩn trọng, tuân thủ quy trình và hệ thống hóa thông tin."
        }
    }

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = load_question_config()
        self.config = config
        self.questions = config.get("questions", [])
        self.dimensions = config.get("dimensions", {})

    def evaluate(self, answers: Dict[str, int]) -> Dict[str, Any]:
        """
        Đánh giá kết quả từ bộ câu trả lời `answers`: {question_id: int_val} (với int_val từ 1 đến 5).
        """
        # 1. Validation check (Straight-lining)
        total_questions = len(self.questions)
        answered_count = len(answers)
        straight_lining = False

        if answered_count > 0:
            val_counts = {}
            for v in answers.values():
                val_counts[v] = val_counts.get(v, 0) + 1
            max_same = max(val_counts.values()) if val_counts else 0
            if max_same / answered_count >= 0.9 and answered_count >= 10:
                straight_lining = True

        # 2. RIASEC Scoring
        riasec_scores = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}
        riasec_counts = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}

        for q in self.questions:
            if q.get("section") == "riasec":
                trait = q.get("trait")
                val = answers.get(q["id"], 3)
                riasec_scores[trait] = riasec_scores.get(trait, 0) + val
                riasec_counts[trait] = riasec_counts.get(trait, 0) + 1

        riasec_percent = {}
        for trait, raw in riasec_scores.items():
            count = riasec_counts[trait] or 4
            min_pos = count * 1
            max_pos = count * 5
            rng = max_pos - min_pos
            pct = round((raw - min_pos) / rng * 100, 1) if rng > 0 else 0
            riasec_percent[trait] = pct

        tie_break_order = ["R", "I", "A", "S", "E", "C"]
        sorted_riasec = sorted(
            riasec_scores.keys(),
            key=lambda t: (riasec_scores[t], -tie_break_order.index(t)),
            reverse=True
        )

        holland_code = "".join(sorted_riasec[:3])
        primary_trait = sorted_riasec[0]
        secondary_trait = sorted_riasec[1]

        max_score = riasec_scores[sorted_riasec[0]]
        min_score = riasec_scores[sorted_riasec[-1]]
        low_differentiation = (max_score - min_score) < 4
        all_low = max_score < 10

        # 3. MBTI Scoring
        mbti_poles = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
        for q in self.questions:
            if q.get("section") == "mbti":
                pole = q.get("pole")
                val = answers.get(q["id"], 3)
                mbti_poles[pole] = mbti_poles.get(pole, 0) + val

        mbti_result = []
        mbti_details = {}
        pair_defaults = [("E", "I"), ("S", "N"), ("T", "F"), ("J", "P")]

        for p1, p2 in pair_defaults:
            s1 = mbti_poles.get(p1, 0)
            s2 = mbti_poles.get(p2, 0)
            diff = abs(s1 - s2)
            strength_pct = round(diff / 8 * 100, 1)

            if s1 > s2:
                winner = p1
            elif s2 > s1:
                winner = p2
            else:
                winner = p2 # Tie breaker

            mbti_result.append(winner)
            mbti_details[f"{p1}{p2}"] = {
                "winner": winner,
                f"score_{p1}": s1,
                f"score_{p2}": s2,
                "strength_pct": strength_pct,
                "is_tie": s1 == s2
            }

        mbti_code = "".join(mbti_result)

        # 4. Sector Recommendation
        primary_sector_info = self.SECTOR_RULES.get(primary_trait, self.SECTOR_RULES["I"])
        secondary_sector_info = self.SECTOR_RULES.get(secondary_trait, self.SECTOR_RULES["S"])

        trait_names_vi = {
            "R": "Kỹ thuật – Thực tế",
            "I": "Nghiên cứu – Phân tích",
            "A": "Nghệ thuật – Sáng tạo",
            "S": "Xã hội – Hỗ trợ",
            "E": "Quản lý – Thuyết phục",
            "C": "Nghiệp vụ – Tổ chức"
        }

        warnings = []
        if straight_lining:
            warnings.append("⚠️ Cảnh báo: Các lựa chọn của bạn có xu hướng lặp lại giống hệt nhau (≥ 90%). Kết quả có thể chưa phản ánh chính xác nhất.")
        if low_differentiation:
            warnings.append("💡 Thông tin: Độ chênh lệch giữa các nhóm sở thích khá nhỏ (< 4 điểm). Bạn sở hữu sở thích đa dạng.")
        if all_low:
            warnings.append("💡 Thông tin: Điểm các nhóm sở thích đều ở mức thấp (< 10 điểm). Bạn nên thực hiện lại bài kiểm tra cẩn thận hơn.")

        return {
            "summary": {
                "holland_code": holland_code,
                "primary_trait": primary_trait,
                "primary_trait_name": trait_names_vi.get(primary_trait, ""),
                "secondary_trait": secondary_trait,
                "secondary_trait_name": trait_names_vi.get(secondary_trait, ""),
                "mbti_code": mbti_code,
                "answered_questions": answered_count,
                "total_questions": total_questions
            },
            "riasec_scores": riasec_scores,
            "riasec_percent": riasec_percent,
            "mbti_details": mbti_details,
            "primary_sector": primary_sector_info,
            "secondary_sector": secondary_sector_info,
            "warnings": warnings
        }


def rule_based_bot(user_input: str) -> str:
    """Hàm giao tiếp cơ bản (Backward compatibility)"""
    text = user_input.lower()
    if "hướng nghiệp" in text or "trắc nghiệm" in text or "ngành" in text:
        return "Chào bạn! Đây là Rule-Based Bot Hướng nghiệp (Cấp độ 1). Bạn có thể mở giao diện Web tông màu trắng để hoàn thành 40 câu hỏi trắc nghiệm!"
    elif "chào" in text or "hi" in text or "hello" in text:
        return "Xin chào! Tôi là Rule-Based Career Bot (Cấp độ 1). Tôi hỗ trợ phân tích nhóm ngành dựa trên bài trắc nghiệm."
    elif "giá" in text or "chi phí" in text:
        return "Bài trắc nghiệm hướng nghiệp Cấp độ 1 hoàn toàn miễn phí!"
    elif "liên hệ" in text or "hotline" in text:
        return "Hotline hỗ trợ: 1900-1234, Email: support@vinuni.edu.vn"
    else:
        return "Xin lỗi, tôi là Rule-Based Bot (Cấp độ 1). Hãy chạy ứng dụng Web để thực hiện bài trắc nghiệm hướng nghiệp đầy đủ!"


class WhiteThemeWebHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler phục vụ Giao diện Người dùng tông màu trắng (White Theme UI)"""
    
    config_data = load_question_config()
    engine = RuleBasedCareerEngine(config_data)

    def do_GET(self):
        if self.path == "/" or self.path.startswith("/index.html"):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            html_content = self.generate_white_theme_html()
            self.wfile.write(html_content.encode("utf-8"))
        elif self.path == "/api/questions":
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(self.config_data, ensure_ascii=False).encode("utf-8"))
        else:
            self.send_error(404, "Page Not Found")

    def do_POST(self):
        if self.path == "/api/evaluate":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            try:
                payload = json.loads(post_data.decode("utf-8"))
                answers = payload.get("answers", {})
                result = self.engine.evaluate(answers)
                
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_error(404, "API Endpoint Not Found")

    def generate_white_theme_html(self) -> str:
        """Tạo mã HTML/CSS/JS cho Giao diện người dùng tông màu trắng tinh tế"""
        return """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hệ Thống Hướng Nghiệp AI - Rule-Based (Level 1)</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --accent-blue: #2563eb;
            --accent-hover: #1d4ed8;
            --accent-light: #eff6ff;
            --border-color: #e2e8f0;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.05);
            --shadow-md: 0 4px 20px -2px rgba(0,0,0,0.06);
            --radius-lg: 16px;
            --radius-md: 10px;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
        }

        body {
            background-color: var(--bg-primary);
            color: var(--text-main);
            line-height: 1.6;
            padding-bottom: 60px;
        }

        .header {
            background: #ffffff;
            border-bottom: 1px solid var(--border-color);
            padding: 24px 0;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: var(--shadow-sm);
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 0 20px;
        }

        .header-content {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .logo-area h1 {
            font-size: 1.35rem;
            font-weight: 700;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .badge {
            background: var(--accent-light);
            color: var(--accent-blue);
            font-size: 0.75rem;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 20px;
            border: 1px solid #bfdbfe;
        }

        .progress-bar-container {
            margin-top: 15px;
            background: #f1f5f9;
            height: 8px;
            border-radius: 4px;
            overflow: hidden;
        }

        .progress-bar-fill {
            background: var(--accent-blue);
            height: 100%;
            width: 0%;
            transition: width 0.3s ease;
        }

        .quick-tools {
            display: flex;
            gap: 10px;
            margin: 20px 0;
            justify-content: flex-end;
        }

        .btn-secondary {
            background: #ffffff;
            color: var(--text-muted);
            border: 1px solid var(--border-color);
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }

        .btn-secondary:hover {
            background: #f1f5f9;
            color: var(--text-main);
        }

        .section-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: var(--shadow-md);
        }

        .section-title {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 16px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .question-item {
            padding: 16px 0;
            border-bottom: 1px dashed var(--border-color);
        }

        .question-item:last-child {
            border-bottom: none;
        }

        .question-text {
            font-size: 0.95rem;
            font-weight: 500;
            margin-bottom: 12px;
            color: #334155;
        }

        .options-group {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 8px;
        }

        @media (max-width: 640px) {
            .options-group {
                grid-template-columns: 1fr;
            }
        }

        .option-label {
            background: #f8fafc;
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 10px 6px;
            font-size: 0.8rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
            user-select: none;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            color: var(--text-muted);
        }

        .option-label:hover {
            border-color: #93c5fd;
            background: #eff6ff;
            color: var(--accent-blue);
        }

        .option-label input {
            display: none;
        }

        .option-label.selected {
            background: var(--accent-blue);
            color: #ffffff;
            border-color: var(--accent-blue);
            font-weight: 600;
        }

        .btn-submit {
            width: 100%;
            background: var(--accent-blue);
            color: #ffffff;
            border: none;
            padding: 16px;
            border-radius: var(--radius-lg);
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 4px 14px rgba(37,99,235,0.3);
            transition: all 0.2s;
            margin-top: 10px;
        }

        .btn-submit:hover {
            background: var(--accent-hover);
            transform: translateY(-1px);
        }

        /* RESULT VIEW STYLES */
        .result-container {
            display: none;
        }

        .result-header-card {
            background: #ffffff;
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 30px;
            margin-bottom: 24px;
            box-shadow: var(--shadow-md);
            text-align: center;
        }

        .sector-highlight-box {
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            border-radius: var(--radius-lg);
            padding: 24px;
            margin: 20px 0;
            text-align: left;
        }

        .sector-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--accent-blue);
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .code-pill {
            background: #ffffff;
            border: 1px solid #cbd5e1;
            padding: 4px 12px;
            border-radius: 6px;
            font-weight: 700;
            color: #1e293b;
            font-size: 0.9rem;
        }

        .tag-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 12px;
        }

        .tag-item {
            background: #ffffff;
            color: #334155;
            border: 1px solid var(--border-color);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }

        .chart-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 24px;
        }

        @media (max-width: 768px) {
            .chart-row {
                grid-template-columns: 1fr;
            }
        }

        .score-bar-item {
            margin-bottom: 12px;
        }

        .score-bar-label {
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            font-weight: 500;
            margin-bottom: 4px;
        }

        .bar-bg {
            background: #f1f5f9;
            height: 10px;
            border-radius: 5px;
            overflow: hidden;
        }

        .bar-fill {
            background: var(--accent-blue);
            height: 100%;
            border-radius: 5px;
        }

        .warning-box {
            background: #fffbeb;
            border: 1px solid #fef08a;
            color: #92400e;
            padding: 14px;
            border-radius: 10px;
            font-size: 0.85rem;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>

    <header class="header">
        <div class="container">
            <div class="header-content">
                <div class="logo-area">
                    <h1>🎓 Career Advisor AI <span class="badge">Rule-Based Level 1</span></h1>
                </div>
                <div style="font-size:0.85rem; color:var(--text-muted);" id="answered-counter">
                    Đã trả lời: 0 / 40
                </div>
            </div>
            <div class="progress-bar-container">
                <div class="progress-bar-fill" id="progress-fill"></div>
            </div>
        </div>
    </header>

    <div class="container" style="margin-top: 24px;">

        <!-- INPUT FORM VIEW -->
        <div id="quiz-view">
            <div class="quick-tools">
                <button class="btn-secondary" onclick="autoFill(4)">⚡ Demo: Chọn Khá Đúng (4)</button>
                <button class="btn-secondary" onclick="autoFillRandom()">🎲 Demo: Random Chọn</button>
                <button class="btn-secondary" onclick="resetForm()">🔄 Làm lại</button>
            </div>

            <form id="quiz-form">
                <div id="questions-wrapper">
                    <div style="text-align:center; padding: 40px; color: var(--text-muted);">
                        ⏳ Đang tải bộ 40 câu hỏi trắc nghiệm từ file config/question.json...
                    </div>
                </div>

                <button type="submit" class="btn-submit">📊 XEM KẾT QUẢ ĐÁNH GIÁ NHÓM NGÀNH PHÙ HỢP</button>
            </form>
        </div>

        <!-- OUTPUT RESULT VIEW -->
        <div id="result-view" class="result-container">
            <div class="quick-tools">
                <button class="btn-secondary" onclick="backToQuiz()">⬅️ Làm lại bài kiểm tra</button>
            </div>

            <div class="result-header-card">
                <h2>🎯 KẾT QUẢ ĐÁNH GIÁ HƯỚNG NGHIỆP CỦA BẠN</h2>
                <p style="color:var(--text-muted); margin-top:6px;">Dựa trên phân tích Luật cố định RIASEC (Holland Code) + MBTI</p>
                <div style="display:flex; justify-content:center; gap:15px; margin-top:15px;">
                    <div class="code-pill">Mã Holland: <span id="res-holland" style="color:var(--accent-blue);">---</span></div>
                    <div class="code-pill">Tính cách MBTI: <span id="res-mbti" style="color:var(--accent-blue);">---</span></div>
                </div>
            </div>

            <div id="warnings-wrapper"></div>

            <!-- PRIMARY SECTOR CARD -->
            <div class="section-card">
                <div class="section-title">⭐ NHÓM NGÀNH CHÍNH PHÙ HỢP NHẤT</div>
                <div class="sector-highlight-box">
                    <div class="sector-title" id="res-primary-name">...</div>
                    <p style="color:#475569; font-size:0.95rem; margin-top:8px;" id="res-primary-desc">...</p>
                </div>

                <div style="margin-top:16px;">
                    <strong style="font-size:0.9rem; color:var(--text-main);">👨‍💻 Các vị trí công việc tiêu biểu:</strong>
                    <div class="tag-grid" id="res-primary-careers"></div>
                </div>

                <div style="margin-top:16px;">
                    <strong style="font-size:0.9rem; color:var(--text-main);">📚 Ngành học đại học gợi ý:</strong>
                    <div class="tag-grid" id="res-primary-majors"></div>
                </div>

                <div style="margin-top:16px; background:#f8fafc; padding:14px; border-radius:10px; font-size:0.85rem; color:#475569;">
                    <strong>🏢 Môi trường làm việc:</strong> <span id="res-primary-env">...</span><br>
                    <strong>⚡ Phong cách làm việc:</strong> <span id="res-primary-style">...</span>
                </div>
            </div>

            <!-- SECONDARY SECTOR CARD -->
            <div class="section-card">
                <div class="section-title">🔹 NHÓM NGÀNH BỔ TRỢ (ALTERNATIVE)</div>
                <div class="sector-title" style="font-size:1.1rem; color:#334155;" id="res-secondary-name">...</div>
                <p style="color:#64748b; font-size:0.9rem; margin-top:6px;" id="res-secondary-desc">...</p>
            </div>

            <!-- CHARTS ROW -->
            <div class="chart-row">
                <div class="section-card" style="margin-bottom:0;">
                    <div class="section-title">📊 Điểm Số Holland RIASEC</div>
                    <div id="riasec-bars"></div>
                </div>

                <div class="section-card" style="margin-bottom:0;">
                    <div class="section-title">🧩 Phân Tích Tính Cách MBTI</div>
                    <div id="mbti-bars"></div>
                </div>
            </div>
        </div>

    </div>

    <script>
        let questionsData = [];
        let answersState = {};

        document.addEventListener("DOMContentLoaded", () => {
            fetchQuestions();
            document.getElementById("quiz-form").addEventListener("submit", handleSubmit);
        });

        async function fetchQuestions() {
            try {
                const res = await fetch("/api/questions");
                const data = await res.json();
                questionsData = data.questions || [];
                renderQuestions(questionsData);
            } catch (err) {
                console.error("Lỗi tải câu hỏi:", err);
            }
        }

        function renderQuestions(questions) {
            const wrapper = document.getElementById("questions-wrapper");
            wrapper.innerHTML = "";

            let currentSection = "";
            let sectionCard = null;

            const scaleLabels = [
                { val: 1, label: "1. Không đúng" },
                { val: 2, label: "2. Ít đúng" },
                { val: 3, label: "3. Trung lập" },
                { val: 4, label: "4. Khá đúng" },
                { val: 5, label: "5. Rất đúng" }
            ];

            questions.forEach((q, idx) => {
                const secTitle = q.section === "riasec" 
                    ? "PHẦN 1: SỞ THÍCH NGHỀ NGHIỆP (RIASEC)" 
                    : "PHẦN 2: PHONG CÁCH TÍNH CÁCH (MBTI)";

                if (secTitle !== currentSection) {
                    currentSection = secTitle;
                    sectionCard = document.createElement("div");
                    sectionCard.className = "section-card";
                    sectionCard.innerHTML = `<div class="section-title">${currentSection}</div>`;
                    wrapper.appendChild(sectionCard);
                }

                const item = document.createElement("div");
                item.className = "question-item";
                item.innerHTML = `
                    <div class="question-text">Câu ${q.order || idx + 1}: ${q.text}</div>
                    <div class="options-group">
                        ${scaleLabels.map(opt => `
                            <label class="option-label" id="lbl_${q.id}_${opt.val}">
                                <input type="radio" name="q_${q.id}" value="${opt.val}" onchange="selectOption('${q.id}', ${opt.val})">
                                <span>${opt.label}</span>
                            </label>
                        `).join('')}
                    </div>
                `;
                sectionCard.appendChild(item);
            });
        }

        function selectOption(qId, val) {
            answersState[qId] = val;

            for (let i = 1; i <= 5; i++) {
                const lbl = document.getElementById(`lbl_${qId}_${i}`);
                if (lbl) {
                    if (i === val) lbl.classList.add("selected");
                    else lbl.classList.remove("selected");
                }
            }

            updateProgress();
        }

        function updateProgress() {
            const total = questionsData.length || 40;
            const answered = Object.keys(answersState).length;
            const pct = Math.round((answered / total) * 100);

            document.getElementById("answered-counter").innerText = `Đã trả lời: ${answered} / ${total}`;
            document.getElementById("progress-fill").style.width = `${pct}%`;
        }

        function autoFill(val) {
            questionsData.forEach(q => {
                selectOption(q.id, val);
                const radio = document.querySelector(`input[name="q_${q.id}"][value="${val}"]`);
                if (radio) radio.checked = true;
            });
        }

        function autoFillRandom() {
            questionsData.forEach(q => {
                const randVal = Math.floor(Math.random() * 5) + 1;
                selectOption(q.id, randVal);
                const radio = document.querySelector(`input[name="q_${q.id}"][value="${randVal}"]`);
                if (radio) radio.checked = true;
            });
        }

        function resetForm() {
            answersState = {};
            document.querySelectorAll(".option-label").forEach(l => l.classList.remove("selected"));
            document.querySelectorAll("input[type='radio']").forEach(r => r.checked = false);
            updateProgress();
        }

        async function handleSubmit(e) {
            e.preventDefault();

            try {
                const res = await fetch("/api/evaluate", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ answers: answersState })
                });

                const result = await res.json();
                renderResult(result);
            } catch (err) {
                alert("Lỗi tính toán kết quả: " + err);
            }
        }

        function renderResult(res) {
            document.getElementById("quiz-view").style.display = "none";
            document.getElementById("result-view").style.display = "block";
            window.scrollTo({ top: 0, behavior: 'smooth' });

            const summary = res.summary || {};
            document.getElementById("res-holland").innerText = summary.holland_code || "---";
            document.getElementById("res-mbti").innerText = summary.mbti_code || "---";

            // Warnings
            const warnWrapper = document.getElementById("warnings-wrapper");
            warnWrapper.innerHTML = "";
            (res.warnings || []).forEach(w => {
                const box = document.createElement("div");
                box.className = "warning-box";
                box.innerText = w;
                warnWrapper.appendChild(box);
            });

            // Primary Sector
            const pSec = res.primary_sector || {};
            document.getElementById("res-primary-name").innerText = `${pSec.icon || ''} ${pSec.name || ''}`;
            document.getElementById("res-primary-desc").innerText = pSec.description || '';
            document.getElementById("res-primary-env").innerText = pSec.environment || '';
            document.getElementById("res-primary-style").innerText = pSec.work_style || '';

            document.getElementById("res-primary-careers").innerHTML = (pSec.careers || [])
                .map(c => `<span class="tag-item">${c}</span>`).join('');
            document.getElementById("res-primary-majors").innerHTML = (pSec.majors || [])
                .map(m => `<span class="tag-item" style="background:#eff6ff; color:#1d4ed8;">${m}</span>`).join('');

            // Secondary Sector
            const sSec = res.secondary_sector || {};
            document.getElementById("res-secondary-name").innerText = `${sSec.icon || ''} ${sSec.name || ''}`;
            document.getElementById("res-secondary-desc").innerText = sSec.description || '';

            // RIASEC Bars
            const riasecBars = document.getElementById("riasec-bars");
            riasecBars.innerHTML = "";
            const traitNames = {
                R: "Realistic (Thực tế)",
                I: "Investigative (Nghiên cứu)",
                A: "Artistic (Sáng tạo)",
                S: "Social (Xã hội)",
                E: "Enterprising (Quản lý)",
                C: "Conventional (Nghiệp vụ)"
            };

            const pcts = res.riasec_percent || {};
            Object.keys(pcts).forEach(t => {
                const pct = pcts[t] || 0;
                riasecBars.innerHTML += `
                    <div class="score-bar-item">
                        <div class="score-bar-label">
                            <span>${traitNames[t] || t}</span>
                            <span>${pct}%</span>
                        </div>
                        <div class="bar-bg">
                            <div class="bar-fill" style="width: ${pct}%;"></div>
                        </div>
                    </div>
                `;
            });

            // MBTI Bars
            const mbtiBars = document.getElementById("mbti-bars");
            mbtiBars.innerHTML = "";
            const mbtiDet = res.mbti_details || {};
            Object.keys(mbtiDet).forEach(dim => {
                const item = mbtiDet[dim];
                mbtiBars.innerHTML += `
                    <div class="score-bar-item">
                        <div class="score-bar-label">
                            <span>Cặp ${dim}: Kết quả <strong>${item.winner}</strong></span>
                            <span>Độ ưu trội: ${item.strength_pct}%</span>
                        </div>
                        <div class="bar-bg">
                            <div class="bar-fill" style="width: ${item.strength_pct}%; background:#059669;"></div>
                        </div>
                    </div>
                `;
            });
        }

        function backToQuiz() {
            document.getElementById("result-view").style.display = "none";
            document.getElementById("quiz-view").style.display = "block";
        }
    </script>
</body>
</html>
"""


def start_web_server(port: int = 8080):
    """Khởi chạy máy chủ Web tông màu trắng cho Cấp độ 1"""
    server_address = ("", port)
    httpd = HTTPServer(server_address, WhiteThemeWebHandler)
    url = f"http://localhost:{port}"
    print("\n" + "="*60)
    print("🚀 HE THONG HUONG NGHIEP RULE-BASED (LEVEL 1) DANG CHAY!")
    print(f"🌐 Giao diện Web (Tông màu trắng): {url}")
    print("="*60 + "\n")
    
    try:
        webbrowser.open(url)
    except Exception:
        pass
        
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Đã dừng máy chủ Web.")


if __name__ == "__main__":
    # Đảm bảo in Tiếng Việt trên Windows console không lỗi
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    print("=== DEMO CẤP ĐỘ 1: RULE-BASED CAREER ADVISOR ===")
    
    # 1. Chạy CLI Test thử nghiệm
    config = load_question_config()
    engine = RuleBasedCareerEngine(config)
    
    sample_answers = {q["id"]: 4 for q in config.get("questions", [])}
    sample_result = engine.evaluate(sample_answers)
    
    print("\n--- TEST KẾT QUẢ ĐÁNH GIÁ CHẨN MẪU (Sample Input: All 4s) ---")
    print(f"📌 Holland Code: {sample_result['summary']['holland_code']}")
    print(f"📌 MBTI Type: {sample_result['summary']['mbti_code']}")
    print(f"🎯 Nhóm ngành chính: {sample_result['primary_sector']['name']}")
    print(f"💼 Vị trí công việc tiêu biểu: {', '.join(sample_result['primary_sector']['careers'][:3])}")
    print("------------------------------------------------------------\n")
    
    # 2. Khởi chạy Giao diện Web tông màu trắng đơn giản
    start_web_server(8080)
