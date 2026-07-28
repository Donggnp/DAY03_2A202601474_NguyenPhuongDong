"""
🤖 CẤP ĐỘ 1: RULE-BASED CAREER ADVISOR (Hệ thống Hướng nghiệp Dựa trên Luật Cố định)
- Đầu vào (Input): Bộ câu hỏi trắc nghiệm từ `config/question.json` (RIASEC + MBTI)
- Xử lý (Logic): Đánh giá điểm RIASEC & MBTI bằng tập luật rule-based (If/Else, Scoring Matrix)
- Đầu ra (Output): Holland Code, MBTI Type, Nhóm ngành phù hợp & Chi tiết vị trí công việc từ `config/careers.json`
- Giao diện (UI): Streamlit tông màu trắng tinh tế, hiện đại, dễ thao tác
"""

import json
import os
import sys
import subprocess
from typing import Dict, Any, List, Tuple

# Path Constants
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG_QUESTION_PATH = os.path.join(BASE_DIR, "config", "question.json")
CONFIG_CAREERS_PATH = os.path.join(BASE_DIR, "config", "careers.json")


def load_question_config() -> Dict[str, Any]:
    """Tải bộ câu hỏi trắc nghiệm từ config/question.json"""
    if os.path.exists(CONFIG_QUESTION_PATH):
        with open(CONFIG_QUESTION_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    raise FileNotFoundError(f"Không tìm thấy file cấu hình tại: {CONFIG_QUESTION_PATH}")


def load_careers_config() -> Dict[str, Any]:
    """Tải dữ liệu ngành nghề chi tiết từ config/careers.json"""
    if os.path.exists(CONFIG_CAREERS_PATH):
        with open(CONFIG_CAREERS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


# ---------------------------------------------------------------------------
# CORE RULE-BASED ENGINE LOGIC
# ---------------------------------------------------------------------------

def evaluate_riasec(answers: Dict[str, int], questions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Tính điểm RIASEC từ tập câu trả lời Likert (1-5)
    """
    riasec_scores = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}
    riasec_counts = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}

    for q in questions:
        if q.get("section") == "riasec":
            trait = q.get("trait")
            qid = q.get("id")
            val = answers.get(qid, 3)  # Mặc định trung lập 3 nếu chưa trả lời
            if trait in riasec_scores:
                riasec_scores[trait] += val
                riasec_counts[trait] += 1

    # Normalize (% = (raw - min) / range * 100)
    percentages = {}
    for trait in riasec_scores:
        count = riasec_counts[trait] if riasec_counts[trait] > 0 else 4
        min_score = count * 1
        max_score = count * 5
        raw = riasec_scores[trait]
        pct = round(((raw - min_score) / (max_score - min_score)) * 100, 1) if max_score > min_score else 0
        percentages[trait] = pct

    # Sắp xếp lấy 3 trait cao nhất (Holland Code)
    sorted_traits = sorted(riasec_scores.keys(), key=lambda t: (riasec_scores[t], -ord(t)), reverse=True)
    holland_code = "".join(sorted_traits[:3])

    # Kiểm tra độ phân hóa (Confidence check)
    max_val = max(riasec_scores.values())
    min_val = min(riasec_scores.values())
    diff = max_val - min_val
    confidence = "Cao"
    if diff < 4:
        confidence = "Thấp (Kết quả có sự cân bằng giữa các nhóm, nên tham vấn thêm)"
    elif max_val < 10:
        confidence = "Trung bình (Điểm số tổng thể khá thấp)"

    return {
        "raw_scores": riasec_scores,
        "percentages": percentages,
        "sorted_traits": sorted_traits,
        "holland_code": holland_code,
        "confidence": confidence,
        "diff": diff
    }


def evaluate_mbti(answers: Dict[str, int], questions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Tính toán MBTI rút gọn (EI, SN, TF, JP) dựa trên luật so sánh 2 cực
    """
    poles_scores = {
        "E": 0, "I": 0,
        "S": 0, "N": 0,
        "T": 0, "F": 0,
        "J": 0, "P": 0
    }

    for q in questions:
        if q.get("section") == "mbti":
            pole = q.get("pole")
            qid = q.get("id")
            val = answers.get(qid, 3)
            if pole in poles_scores:
                poles_scores[pole] += val

    # So sánh từng cặp pole
    def pick_pole(p1: str, p2: str, default: str) -> Tuple[str, float]:
        s1, s2 = poles_scores[p1], poles_scores[p2]
        total = s1 + s2 if (s1 + s2) > 0 else 1
        if s1 > s2:
            return p1, round((s1 / total) * 100, 1)
        elif s2 > s1:
            return p2, round((s2 / total) * 100, 1)
        else:
            return default, 50.0

    ei, ei_pct = pick_pole("E", "I", "I")
    sn, sn_pct = pick_pole("S", "N", "N")
    tf, tf_pct = pick_pole("T", "F", "F")
    jp, jp_pct = pick_pole("J", "P", "P")

    mbti_code = f"{ei}{sn}{tf}{jp}"

    return {
        "mbti_code": mbti_code,
        "poles_scores": poles_scores,
        "details": {
            "EI": {"selected": ei, "percentage": ei_pct, "raw": (poles_scores["E"], poles_scores["I"])},
            "SN": {"selected": sn, "percentage": sn_pct, "raw": (poles_scores["S"], poles_scores["N"])},
            "TF": {"selected": tf, "percentage": tf_pct, "raw": (poles_scores["T"], poles_scores["F"])},
            "JP": {"selected": jp, "percentage": jp_pct, "raw": (poles_scores["J"], poles_scores["P"])}
        }
    }


def map_career_recommendations(holland_code: str, mbti_code: str, riasec_sorted: List[str]) -> Dict[str, Any]:
    """
    Quy tắc Rule-Based suy luận nhóm ngành phù hợp từ RIASEC + MBTI
    """
    primary = riasec_sorted[0]
    secondary = riasec_sorted[1]
    top_pair = f"{primary}{secondary}"

    recommendations = []

    # RULE MATRIX TABLE
    rules = [
        # REALISTIC (R)
        {
            "condition": lambda p, s: p == "R" and s in ["I", "C"],
            "industry": "Kỹ thuật, Cơ khí, Tự động hóa & Ô tô",
            "careers": ["cơ điện tử", "kỹ thuật điện điện tử", "công nghệ ô tô"],
            "description": "Thích thao tác thiết bị, vận hành máy móc, ứng dụng tư duy kỹ thuật thực tế.",
            "mbti_fit": "Phù hợp phong cách làm việc cẩn trọng, thực tế (ST / NT)."
        },
        {
            "condition": lambda p, s: p == "R" and s in ["A", "S", "E"],
            "industry": "Thiết kế Không gian, Đô thị & Công nghệ Ứng dụng",
            "careers": ["kiến trúc", "nông nghiệp công nghệ cao"],
            "description": "Kết hợp thực hành kỹ thuật với sáng tạo không gian hoặc thiên nhiên.",
            "mbti_fit": "Phù hợp công việc có tính trải nghiệm linh hoạt."
        },

        # INVESTIGATIVE (I)
        {
            "condition": lambda p, s: p == "I" and s in ["R", "C"],
            "industry": "Công nghệ Thông tin, Dữ liệu & AI",
            "careers": ["công nghệ thông tin", "khoa học dữ liệu"],
            "description": "Đam mê giải quyết bài toán phức tạp, phân tích dữ liệu và lập trình hệ thống.",
            "mbti_fit": "Tối ưu với phong cách tư duy logic, phân tích sâu (INTJ, INTP, ISTJ)."
        },
        {
            "condition": lambda p, s: p == "I" and s in ["S", "A"],
            "industry": "Y Dược, Sinh học & Phân tích Nghiên cứu",
            "careers": ["y khoa", "dược học", "công nghệ sinh học", "tâm lý học"],
            "description": "Tìm tòi tri thức khoa học để ứng dụng chăm sóc sức khỏe và con người.",
            "mbti_fit": "Phù hợp người chu đáo, ham học hỏi và nghiên cứu (INFJ, INTJ, INFP)."
        },

        # ARTISTIC (A)
        {
            "condition": lambda p, s: p == "A" and s in ["I", "E", "S"],
            "industry": "Sáng tạo Mỹ thuật, Truyền thông & Thiết kế",
            "careers": ["thiết kế đồ họa", "truyền thông đa phương tiện", "thiết kế thời trang"],
            "description": "Khả năng tư duy thẩm mỹ vượt trội, tự do biểu đạt ý tưởng qua thị giác và âm thanh.",
            "mbti_fit": "Tối ưu cho người linh hoạt, giàu trí tưởng tượng (ENFP, INFP, ENTP)."
        },
        {
            "condition": lambda p, s: p == "A" and s in ["R", "C"],
            "industry": "Thiết kế Nội thất, Kiến trúc & Báo chí",
            "careers": ["kiến trúc", "báo chí"],
            "description": "Kết hợp giữa ý tưởng nghệ thuật cá nhân và tính nguyên tắc thực thi.",
            "mbti_fit": "Tốt cho công việc cần sáng tạo nhưng có cấu trúc."
        },

        # SOCIAL (S)
        {
            "condition": lambda p, s: p == "S" and s in ["E", "A"],
            "industry": "Giáo dục, Đào tạo, Truyền thông & Ngoại giao",
            "careers": ["sư phạm", "quan hệ công chúng", "ngôn ngữ anh"],
            "description": "Yêu thích tương tác con người, giảng dạy, kết nối cộng đồng và ngoại ngữ.",
            "mbti_fit": "Thích hợp phong cách hướng ngoại, thấu cảm (ENFJ, ESFJ, ENFP)."
        },
        {
            "condition": lambda p, s: p == "S" and s in ["I", "C"],
            "industry": "Y Tế Chăm Sóc, Điều Dưỡng & Tư Vấn Tâm Lý",
            "careers": ["điều dưỡng", "tâm lý học", "y khoa"],
            "description": "Chu đáo, kiên nhẫn, thích giúp đỡ và tham vấn cho người khác.",
            "mbti_fit": "Lý tưởng cho người thấu hiểu, tận tâm (ISFJ, INFJ)."
        },

        # ENTERPRISING (E)
        {
            "condition": lambda p, s: p == "E" and s in ["S", "C", "A"],
            "industry": "Quản trị Kinh doanh, Marketing & Khởi nghiệp",
            "careers": ["quản trị kinh doanh", "marketing", "thương mại điện tử"],
            "description": "Tư duy lãnh đạo, thuyết phục, nhạy bén thị trường và chấp nhận thử thách.",
            "mbti_fit": "Phù hợp phong cách quyết đoán, năng động (ENTJ, ESTP, ENTP)."
        },
        {
            "condition": lambda p, s: p == "E" and s in ["I", "R"],
            "industry": "Quản trị Khách sạn, Dịch vụ & Du lịch",
            "careers": ["du lịch", "quản trị khách sạn"],
            "description": "Giao tiếp linh hoạt, tổ chức sự kiện và quản lý vận hành dịch vụ cao cấp.",
            "mbti_fit": "Thích hợp môi trường sôi động, đa dạng trải nghiệm (ESFP, ESTP)."
        },

        # CONVENTIONAL (C)
        {
            "condition": lambda p, s: p == "C" and s in ["E", "I"],
            "industry": "Tài chính - Ngân hàng, Kế toán & Logistics",
            "careers": ["kế toán", "tài chính ngân hàng", "logistics"],
            "description": "Cẩn trọng với số liệu, quy trình chuẩn chỉnh, quản lý chuỗi vận hành và hồ sơ.",
            "mbti_fit": "Rất phù hợp người nguyên tắc, kỷ luật (ISTJ, ESTJ, ISFJ)."
        },
        {
            "condition": lambda p, s: p == "C" and s in ["S", "A"],
            "industry": "Quản trị Nhân sự & Pháp lý Doanh nghiệp",
            "careers": ["quản trị nhân sự", "luật"],
            "description": "Theo dõi quy định, chính sách nhân sự, tư vấn luật và duy trì hệ thống.",
            "mbti_fit": "Phù hợp phong cách công bằng, chuẩn mực."
        }
    ]

    # Khớp rule
    matched_industry = None
    recommended_careers = []
    rule_desc = ""
    mbti_desc = ""

    for rule in rules:
        if rule["condition"](primary, secondary):
            matched_industry = rule["industry"]
            recommended_careers = rule["careers"]
            rule_desc = rule["description"]
            mbti_desc = rule["mbti_fit"]
            break

    # Fallback nếu không khớp rule nguyên mẫu
    if not matched_industry:
        fallback_map = {
            "R": ("Kỹ thuật - Công nghệ", ["kỹ thuật điện điện tử", "công nghệ ô tô"]),
            "I": ("Nghiên cứu & Công nghệ", ["công nghệ thông tin", "khoa học dữ liệu"]),
            "A": ("Sáng tạo & Nghệ thuật", ["thiết kế đồ họa", "truyền thông đa phương tiện"]),
            "S": ("Xã hội & Giáo dục", ["sư phạm", "tâm lý học"]),
            "E": ("Kinh doanh & Management", ["quản trị kinh doanh", "marketing"]),
            "C": ("Nghiệp vụ & Tài chính", ["kế toán", "tài chính ngân hàng"])
        }
        matched_industry, recommended_careers = fallback_map.get(primary, ("Công nghệ & Quản trị", ["công nghệ thông tin", "quản trị kinh doanh"]))
        rule_desc = "Được đề xuất dựa trên tính cách ưu trội hàng đầu của bạn."
        mbti_desc = f"Phù hợp với nhóm tính cách {mbti_code}."

    return {
        "matched_industry": matched_industry,
        "recommended_career_keys": recommended_careers,
        "rule_description": rule_desc,
        "mbti_description": mbti_desc,
        "top_pair": top_pair
    }


def process_assessment(answers: Dict[str, int]) -> Dict[str, Any]:
    """Hàm tổng hợp xử lý bài trắc nghiệm đầy đủ"""
    config = load_question_config()
    questions = config.get("questions", [])
    careers_db = load_careers_config()

    riasec_res = evaluate_riasec(answers, questions)
    mbti_res = evaluate_mbti(answers, questions)
    career_res = map_career_recommendations(
        riasec_res["holland_code"],
        mbti_res["mbti_code"],
        riasec_res["sorted_traits"]
    )

    # Lấy thông tin chi tiết các ngành nghề khuyến nghị từ careers.json
    detailed_careers = []
    for key in career_res["recommended_career_keys"]:
        if key in careers_db:
            info = careers_db[key]
            info["key"] = key
            info["ten_nganh"] = key.title()
            detailed_careers.append(info)

    return {
        "riasec": riasec_res,
        "mbti": mbti_res,
        "career_recommendation": career_res,
        "detailed_careers": detailed_careers
    }


# ---------------------------------------------------------------------------
# STREAMLIT UI (CLEAN WHITE THEME)
# ---------------------------------------------------------------------------

def render_streamlit_app():
    import streamlit as st

    # Cấu hình trang với tông màu sáng/trắng
    st.set_page_config(
        page_title="Rule-Based Career Advisor (Level 1)",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # CSS Custom cho Tông màu Trắng Hiện đại, Tinh tế
    st.markdown("""
        <style>
            /* Clean White Theme Overrides */
            .main {
                background-color: #FFFFFF;
                color: #212529;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            }
            .stApp {
                background-color: #FAFAFA;
            }
            
            /* Clean White Container Cards */
            .white-card {
                background-color: #FFFFFF;
                border: 1px solid #E9ECEF;
                border-radius: 12px;
                padding: 24px;
                margin-bottom: 20px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
            }
            
            .header-box {
                background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
                border: 1px solid #E2E8F0;
                border-radius: 16px;
                padding: 28px;
                margin-bottom: 25px;
                text-align: center;
                box-shadow: 0 4px 12px rgba(0,0,0,0.02);
            }
            
            .result-header {
                background: #F8F9FA;
                border-left: 5px solid #2563EB;
                border-radius: 8px;
                padding: 18px 24px;
                margin-bottom: 20px;
            }

            .badge-code {
                display: inline-block;
                background-color: #EFF6FF;
                color: #1D4ED8;
                font-weight: 700;
                font-size: 1.1rem;
                padding: 6px 14px;
                border-radius: 20px;
                border: 1px solid #BFDBFE;
                margin-right: 8px;
            }

            .badge-mbti {
                display: inline-block;
                background-color: #F0FDF4;
                color: #15803D;
                font-weight: 700;
                font-size: 1.1rem;
                padding: 6px 14px;
                border-radius: 20px;
                border: 1px solid #BBF7D0;
            }

            /* Custom Radio Buttons styling */
            div.row-widget.stRadio > div {
                flex-direction: row;
                background-color: #F8F9FA;
                padding: 6px;
                border-radius: 8px;
                border: 1px solid #E9ECEF;
            }
            
            /* Metric text styling */
            .metric-title {
                color: #64748B;
                font-size: 0.85rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            .metric-value {
                color: #0F172A;
                font-size: 1.8rem;
                font-weight: 800;
            }
        </style>
    """, unsafe_allow_html=True)

    # Tải câu hỏi từ config
    try:
        config = load_question_config()
        questions = config.get("questions", [])
        dimensions = config.get("dimensions", {})
    except Exception as e:
        st.error(f"❌ Không thể tải file cấu hình question.json: {e}")
        return

    # Sidebar Header & Info
    with st.sidebar:
        st.image("https://img.icons8.com/illustrations/100/learning.png", width=70)
        st.title("⚙️ Cấu hình Rule-Based")
        st.caption("Level 1: Rule-Based Logic Engine")
        st.divider()

        st.markdown("""
        **📌 Giới thiệu hệ thống:**
        - Sử dụng tập **Rule-Based Matrix** đánh giá trắc nghiệm sở thích (RIASEC) & tính cách (MBTI).
        - **Không phụ thuộc LLM**, đảm bảo tốc độ phản hồi tức thì và đầu ra nhất quán 100%.
        """)
        st.divider()

        st.markdown("### 🚀 Công cụ Kiểm thử Nhanh")
        preset = st.selectbox(
            "Chọn mẫu câu trả lời thử nghiệm:",
            ["-- Tự chọn --", "Mẫu Kỹ thuật & CNTT (R-I)", "Mẫu Sáng tạo & Thiết kế (A)", "Mẫu Kinh doanh & Lãnh đạo (E)", "Đồng đều (Tất cả 4)"]
        )

        st.divider()
        st.info("💡 Mẹo: Nhấn nút **'Đánh giá Kết quả'** ở cuối trang để xem nhóm ngành phù hợp.")

    # Application Header
    st.markdown("""
        <div class="header-box">
            <h1 style="color: #0F172A; margin-bottom: 8px; font-weight: 800;">🎓 HE THONG HUONG NGHIEP RULE-BASED</h1>
            <p style="color: #475569; font-size: 1.1rem; margin-bottom: 0;">
                Khám phá nhóm ngành & định hướng nghề nghiệp phù hợp thông qua thuật toán chuẩn hóa RIASEC & MBTI
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Initialize State Answers
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}

    # Quick fill presets
    if preset == "Mẫu Kỹ thuật & CNTT (R-I)":
        for q in questions:
            qid = q["id"]
            trait = q.get("trait", "")
            pole = q.get("pole", "")
            if trait in ["R", "I"] or pole in ["I", "T", "J"]:
                st.session_state.user_answers[qid] = 5
            elif trait in ["A", "S"] or pole in ["E", "F", "P"]:
                st.session_state.user_answers[qid] = 2
            else:
                st.session_state.user_answers[qid] = 4
    elif preset == "Mẫu Sáng tạo & Thiết kế (A)":
        for q in questions:
            qid = q["id"]
            trait = q.get("trait", "")
            pole = q.get("pole", "")
            if trait in ["A", "I"] or pole in ["N", "F", "P"]:
                st.session_state.user_answers[qid] = 5
            else:
                st.session_state.user_answers[qid] = 2
    elif preset == "Mẫu Kinh doanh & Lãnh đạo (E)":
        for q in questions:
            qid = q["id"]
            trait = q.get("trait", "")
            pole = q.get("pole", "")
            if trait in ["E", "S", "C"] or pole in ["E", "T", "J"]:
                st.session_state.user_answers[qid] = 5
            else:
                st.session_state.user_answers[qid] = 2
    elif preset == "Đồng đều (Tất cả 4)":
        for q in questions:
            st.session_state.user_answers[q["id"]] = 4

    # Tabs for Questionnaire & Results
    tab_questions, tab_results = st.tabs(["📋 BỘ CÂU HỎI TRẮC NGHIỆM (40 CÂU)", "📊 KẾT QUẢ & PHÂN TÍCH NHÓM NGÀNH"])

    with tab_questions:
        st.markdown("##### 📝 Vui lòng đánh giá mức độ phù hợp với bạn theo thang điểm từ 1 (Hoàn toàn không) đến 5 (Hoàn toàn đúng):")
        
        # Split into 2 columns for RIASEC and MBTI
        col_riasec, col_mbti = st.columns([1, 1], gap="large")

        riasec_questions = [q for q in questions if q.get("section") == "riasec"]
        mbti_questions = [q for q in questions if q.get("section") == "mbti"]

        options_map = {
            1: "1 - Hoàn toàn không",
            2: "2 - Ít đúng",
            3: "3 - Trung lập",
            4: "4 - Khá đúng",
            5: "5 - Hoàn toàn đúng"
        }

        with col_riasec:
            st.markdown("""
                <div style="background:#F1F5F9; padding:12px 18px; border-radius:8px; margin-bottom:15px;">
                    <h3 style="margin:0; color:#1E293B; font-size:1.2rem;">🧩 Phần 1: Sở Thích Nghề Nghiệp (RIASEC)</h3>
                </div>
            """, unsafe_allow_html=True)

            for idx, q in enumerate(riasec_questions, start=1):
                qid = q["id"]
                current_val = st.session_state.user_answers.get(qid, 3)
                
                st.markdown(f"**Câu {q['order']}:** {q['text']}")
                selected_val = st.radio(
                    f"Scale_{qid}",
                    options=[1, 2, 3, 4, 5],
                    format_func=lambda x: options_map[x],
                    index=current_val - 1,
                    key=f"radio_{qid}",
                    label_visibility="collapsed"
                )
                st.session_state.user_answers[qid] = selected_val
                st.write("")

        with col_mbti:
            st.markdown("""
                <div style="background:#F1F5F9; padding:12px 18px; border-radius:8px; margin-bottom:15px;">
                    <h3 style="margin:0; color:#1E293B; font-size:1.2rem;">💡 Phần 2: Phong Cách Làm Việc (MBTI)</h3>
                </div>
            """, unsafe_allow_html=True)

            for idx, q in enumerate(mbti_questions, start=1):
                qid = q["id"]
                current_val = st.session_state.user_answers.get(qid, 3)

                st.markdown(f"**Câu {q['order']}:** {q['text']}")
                selected_val = st.radio(
                    f"Scale_{qid}",
                    options=[1, 2, 3, 4, 5],
                    format_func=lambda x: options_map[x],
                    index=current_val - 1,
                    key=f"radio_{qid}",
                    label_visibility="collapsed"
                )
                st.session_state.user_answers[qid] = selected_val
                st.write("")

        st.divider()
        btn_submit = st.button("🚀 CHẨN ĐOÁN & PHÂN TÍCH NHÓM NGÀNH", type="primary", use_container_width=True)

    # Process evaluation when button is clicked or tab switched with answers
    if btn_submit:
        st.toast("✅ Đã tính toán kết quả theo tập luật Rule-Based!")

    # Tab Results Rendering
    with tab_results:
        # Perform assessment
        results = process_assessment(st.session_state.user_answers)
        riasec_res = results["riasec"]
        mbti_res = results["mbti"]
        career_res = results["career_recommendation"]
        detailed_careers = results["detailed_careers"]

        # Top Summary Header
        st.markdown(f"""
            <div class="result-header">
                <div style="margin-bottom:8px;">
                    <span class="badge-code">Holland Code: {riasec_res['holland_code']}</span>
                    <span class="badge-mbti">MBTI: {mbti_res['mbti_code']}</span>
                </div>
                <h2 style="color: #1E293B; margin-top: 10px; margin-bottom: 6px; font-weight:800;">
                    🎯 Nhóm Ngành Phù Hợp Nhất: <span style="color:#2563EB;">{career_res['matched_industry']}</span>
                </h2>
                <p style="color: #475569; font-size: 1rem; margin-bottom:0;">
                    {career_res['rule_description']} {career_res['mbti_description']}
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Overview Metrics Cards
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.markdown("""
                <div class="white-card">
                    <div class="metric-title">Mã Holland Ưu Trội</div>
                    <div class="metric-value" style="color:#2563EB;">{}</div>
                    <div style="font-size:0.85rem; color:#64748B; margin-top:4px;">3 nhóm sở thích cao nhất</div>
                </div>
            """.format(riasec_res['holland_code']), unsafe_allow_html=True)
        with col_m2:
            st.markdown("""
                <div class="white-card">
                    <div class="metric-title">Nhóm Tính Cách MBTI</div>
                    <div class="metric-value" style="color:#16A34A;">{}</div>
                    <div style="font-size:0.85rem; color:#64748B; margin-top:4px;">Phong cách làm việc & giao tiếp</div>
                </div>
            """.format(mbti_res['mbti_code']), unsafe_allow_html=True)
        with col_m3:
            st.markdown("""
                <div class="white-card">
                    <div class="metric-title">Độ Tin Cậy Kết Quả</div>
                    <div class="metric-value" style="color:#D97706; font-size:1.3rem; margin-top:6px;">{}</div>
                    <div style="font-size:0.85rem; color:#64748B; margin-top:4px;">Độ phân hóa điểm số</div>
                </div>
            """.format(riasec_res['confidence']), unsafe_allow_html=True)

        st.divider()

        # Detailed Career Positions
        st.markdown("### 💼 1. Các Vị Trí Ngành Nghề Gợi Ý Khuyên Dùng")
        if detailed_careers:
            cols = st.columns(len(detailed_careers))
            for i, career in enumerate(detailed_careers):
                with cols[i]:
                    st.markdown(f"""
                        <div class="white-card" style="height:100%;">
                            <h4 style="color:#1E3A8A; margin-top:0;">📌 {career['ten_nganh']}</h4>
                            <p style="font-size:0.9rem; color:#334155;"><strong>Mô tả:</strong> {career.get('mo_ta', '')}</p>
                            <p style="font-size:0.9rem; color:#065F46;"><strong>💰 Mức lương:</strong> {career.get('muc_luong', '')}</p>
                            <p style="font-size:0.9rem; color:#1E293B;"><strong>⚡ Kỹ năng cần có:</strong> {career.get('ky_nang', '')}</p>
                            <p style="font-size:0.85rem; color:#475569;"><strong>📈 Triển vọng:</strong> {career.get('trien_vong', '')}</p>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Các vị trí gợi ý: " + ", ".join(career_res['recommended_career_keys']))

        st.divider()

        # Detailed RIASEC & MBTI Charts / Progress
        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            st.markdown("### 📊 Điểm Số Chi Tiết RIASEC")
            riasec_names = dimensions.get("riasec", {})
            for trait, pct in riasec_res["percentages"].items():
                name_vi = riasec_names.get(trait, {}).get("name_vi", trait)
                raw_val = riasec_res["raw_scores"][trait]
                st.markdown(f"**{trait} - {name_vi}** ({raw_val}/20 điểm)")
                st.progress(int(pct) / 100.0, text=f"{pct}%")

        with col_chart2:
            st.markdown("### 🧠 Chi Tiết Các Cặp Tính Cách MBTI")
            mbti_details = mbti_res["details"]
            dim_names = {
                "EI": "Nguồn năng lượng (Hướng ngoại E vs Hướng nội I)",
                "SN": "Tiếp nhận thông tin (Giác quan S vs Trực giác N)",
                "TF": "Ra quyết định (Lý trí T vs Cảm xúc F)",
                "JP": "Lối sống (Nguyên tắc J vs Linh hoạt P)"
            }

            for dim_code, info in mbti_details.items():
                st.markdown(f"**{dim_code}: {dim_names.get(dim_code, '')}**")
                selected = info["selected"]
                pct = info["percentage"]
                raw_e, raw_i = info["raw"]
                st.markdown(f"Cực ưu trội: **{selected}** ({pct}% - Điểm số: {raw_e} vs {raw_i})")
                st.progress(int(pct) / 100.0)


# ---------------------------------------------------------------------------
# CLI / MAIN ENTRY POINT
# ---------------------------------------------------------------------------

def run_cli_demo():
    """Chạy thử nghiệm trên giao diện CLI nếu gọi bằng python trực tiếp"""
    print("=" * 60)
    print("=== DEMO CẤP ĐỘ 1: RULE-BASED CAREER ADVISOR ===")
    print("=" * 60)

    # Tạo mẫu câu trả lời ngẫu nhiên giả định (tất cả 4 điểm)
    config = load_question_config()
    questions = config.get("questions", [])
    sample_answers = {q["id"]: 4 for q in questions}

    # Tính toán kết quả
    res = process_assessment(sample_answers)
    print("\n--- TEST KẾT QUẢ ĐÁNH GIÁ CHẨN MẪU (Sample Input: All 4s) ---")
    print(f"📌 Holland Code: {res['riasec']['holland_code']}")
    print(f"📌 MBTI Type: {res['mbti']['mbti_code']}")
    print(f"🎯 Nhóm ngành chính: {res['career_recommendation']['matched_industry']}")
    print(f"💼 Ngành gợi ý: {', '.join(res['career_recommendation']['recommended_career_keys'])}")
    print("-" * 60)

    # Chạy giao diện Streamlit
    print("\n🚀 Đang khởi chạy giao diện Web Streamlit (Tông màu trắng)...")
    cmd = [sys.executable, "-m", "streamlit", "run", __file__]
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n🛑 Đã dừng ứng dụng Streamlit.")


if __name__ == "__main__":
    # Check if running inside Streamlit
    try:
        import streamlit as st
        # If running via `streamlit run`, st.runtime.exists() is True
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx() is not None:
            render_streamlit_app()
        else:
            run_cli_demo()
    except Exception:
        run_cli_demo()
