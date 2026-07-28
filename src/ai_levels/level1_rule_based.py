"""
🤖 CẤP ĐỘ 1: RULE-BASED CAREER ADVISOR (Hệ thống Hướng nghiệp dựa trên Luật cố định)
Input: Bộ câu hỏi trắc nghiệm trong config/question.json (RIASEC + MBTI)
Output: Holland Code, MBTI Type & Nhóm ngành / Nghề nghiệp phù hợp
Giao diện: Streamlit Web UI (Tông màu Trắng sáng / Clean White Theme)
"""

import os
import sys
import json
import subprocess

# -----------------------------------------------------------------------------
# PATH CONFIGURATION
# -----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QUESTION_PATH = os.path.join(BASE_DIR, "config", "question.json")
CAREERS_PATH = os.path.join(BASE_DIR, "config", "careers.json")

# -----------------------------------------------------------------------------
# RULE-BASED MAPPING RULES (RIASEC & MBTI -> CAREERS)
# -----------------------------------------------------------------------------
CAREER_RULE_MATRIX = {
    "công nghệ thông tin": {"riasec": ["I", "R", "C"], "mbti": ["INTJ", "INTP", "ISTJ", "ENTP"]},
    "khoa học dữ liệu": {"riasec": ["I", "C", "R"], "mbti": ["INTJ", "INTP", "ISTP", "ESTJ"]},
    "thiết kế đồ họa": {"riasec": ["A", "I", "S"], "mbti": ["INFP", "ENFP", "ISFP", "INTP"]},
    "kiến trúc": {"riasec": ["A", "R", "I"], "mbti": ["ISTP", "INTJ", "INFP", "ENTP"]},
    "truyền thông đa phương tiện": {"riasec": ["A", "E", "S"], "mbti": ["ENFP", "ENTP", "ESFP", "ENFJ"]},
    "thiết kế thời trang": {"riasec": ["A", "E", "R"], "mbti": ["ISFP", "INFP", "ENFP", "ESFP"]},
    "quản trị kinh doanh": {"riasec": ["E", "C", "S"], "mbti": ["ESTJ", "ENTJ", "ESFJ", "ENFJ"]},
    "marketing": {"riasec": ["E", "A", "S"], "mbti": ["ENFP", "ENTP", "ENTJ", "ENFJ"]},
    "thương mại điện tử": {"riasec": ["E", "C", "I"], "mbti": ["ENTP", "ESTJ", "ENTJ", "INTP"]},
    "du lịch": {"riasec": ["S", "E", "A"], "mbti": ["ESFP", "ENFP", "ESFJ", "ENFJ"]},
    "quản trị khách sạn": {"riasec": ["S", "E", "C"], "mbti": ["ESFJ", "ESTJ", "ENFJ", "ESFP"]},
    "kế toán": {"riasec": ["C", "I", "R"], "mbti": ["ISTJ", "ISFJ", "ESTJ", "INTJ"]},
    "tài chính ngân hàng": {"riasec": ["C", "E", "I"], "mbti": ["ESTJ", "ENTJ", "ISTJ", "INTJ"]},
    "logistics": {"riasec": ["C", "E", "R"], "mbti": ["ISTJ", "ESTJ", "INTJ", "ISTP"]},
    "quản trị nhân sự": {"riasec": ["S", "E", "C"], "mbti": ["ENFJ", "ESFJ", "INFJ", "ENFP"]},
    "sư phạm": {"riasec": ["S", "A", "I"], "mbti": ["ENFJ", "INFJ", "ESFJ", "INFP"]},
    "tâm lý học": {"riasec": ["S", "I", "A"], "mbti": ["INFJ", "INFP", "ENFJ", "INTJ"]},
    "điều dưỡng": {"riasec": ["S", "R", "C"], "mbti": ["ISFJ", "ESFJ", "INFJ", "ISFP"]},
    "y khoa": {"riasec": ["I", "S", "R"], "mbti": ["INTJ", "ISTJ", "INFJ", "INTP"]},
    "dược học": {"riasec": ["I", "C", "R"], "mbti": ["ISTJ", "INTJ", "ISTP", "INTP"]},
    "công nghệ sinh học": {"riasec": ["I", "R", "C"], "mbti": ["INTP", "INTJ", "ISTP", "ISFP"]},
    "công nghệ thực phẩm": {"riasec": ["C", "I", "R"], "mbti": ["ISTJ", "ISFP", "ESTJ", "INTP"]},
    "công nghệ ô tô": {"riasec": ["R", "C", "I"], "mbti": ["ISTP", "ESTP", "ISTJ", "INTJ"]},
    "kỹ thuật điện điện tử": {"riasec": ["R", "I", "C"], "mbti": ["ISTP", "INTP", "INTJ", "ISTJ"]},
    "cơ điện tử": {"riasec": ["R", "I", "C"], "mbti": ["ISTP", "INTJ", "INTP", "ESTP"]},
    "nông nghiệp công nghệ cao": {"riasec": ["R", "I", "S"], "mbti": ["ISTP", "ISFP", "INTJ", "INTP"]},
    "luật": {"riasec": ["E", "C", "I"], "mbti": ["ENTJ", "INTJ", "ESTJ", "ENFJ"]},
    "quan hệ công chúng": {"riasec": ["E", "S", "A"], "mbti": ["ENFJ", "ENFP", "ENTJ", "ESFP"]},
    "báo chí": {"riasec": ["A", "S", "I"], "mbti": ["ENFP", "INFP", "ENTP", "ENFJ"]},
    "ngôn ngữ anh": {"riasec": ["S", "A", "E"], "mbti": ["ENFP", "INFJ", "ENFJ", "INFP"]}
}

TRAIT_NAMES = {
    "R": "Realistic (Kỹ thuật - Thực tế)",
    "I": "Investigative (Nghiên cứu - Phân tích)",
    "A": "Artistic (Nghệ thuật - Sáng tạo)",
    "S": "Social (Xã hội - Hỗ trợ)",
    "E": "Enterprising (Quản lý - Thuyết phục)",
    "C": "Conventional (Nghiệp vụ - Tổ chức)"
}

MAJOR_GROUPS = {
    "R": "Khối Ngành Kỹ Thuật, Công Nghệ & Sản Xuất",
    "I": "Khối Ngành Nghiên Cứu, Khoa Học & Y Dược",
    "A": "Khối Ngành Sáng Tạo, Thiết Kế & Truyền Thông",
    "S": "Khối Ngành Dịch Vụ Con Người, Giáo Dục & Xã Hội",
    "E": "Khối Ngành Kinh Doanh, Quản Lý & Khởi Nghiệp",
    "C": "Khối Ngành Tài Chính, Kế Toán & Hành Chính"
}

# -----------------------------------------------------------------------------
# DATA LOADERS
# -----------------------------------------------------------------------------
def load_questions() -> dict:
    if os.path.exists(QUESTION_PATH):
        with open(QUESTION_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    raise FileNotFoundError(f"Không tìm thấy file câu hỏi tại: {QUESTION_PATH}")

def load_careers() -> dict:
    if os.path.exists(CAREERS_PATH):
        with open(CAREERS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# -----------------------------------------------------------------------------
# RULE ENGINE CORE LOGIC
# -----------------------------------------------------------------------------
def evaluate_assessment(user_answers: dict) -> dict:
    """
    Hàm tính toán kết quả trắc nghiệm dựa trên tập luật định sẵn.
    user_answers: dict { question_id: score (1..5) }
    """
    question_data = load_questions()
    careers_data = load_careers()
    questions = question_data.get("questions", [])

    # 1. Calc RIASEC
    riasec_scores = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}
    
    # 2. Calc MBTI
    mbti_poles = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}

    for q in questions:
        q_id = q["id"]
        score = int(user_answers.get(q_id, 3)) # Mặc định 3 (Trung lập) nếu chưa chọn
        
        section = q.get("section")
        if section == "riasec":
            trait = q.get("trait")
            if trait in riasec_scores:
                riasec_scores[trait] += score
        elif section == "mbti":
            pole = q.get("pole")
            if pole in mbti_poles:
                mbti_poles[pole] += score

    # Determine Holland Code (Top 3 RIASEC traits)
    sorted_riasec = sorted(riasec_scores.items(), key=lambda x: x[1], reverse=True)
    holland_code = "".join([item[0] for item in sorted_riasec[:3]])

    # Determine MBTI type
    ei = "E" if mbti_poles["E"] > mbti_poles["I"] else "I"
    sn = "S" if mbti_poles["S"] > mbti_poles["N"] else "N"
    tf = "T" if mbti_poles["T"] > mbti_poles["F"] else "F"
    jp = "J" if mbti_poles["J"] > mbti_poles["P"] else "P"
    mbti_type = f"{ei}{sn}{tf}{jp}"

    # Determine Recommended Careers & Major Groups
    recommended_careers = []
    top_traits = [item[0] for item in sorted_riasec[:3]]

    for career_name, rules in CAREER_RULE_MATRIX.items():
        # Score calculation for each career based on rules
        score = 0
        rule_riasec = rules["riasec"]
        rule_mbti = rules["mbti"]

        # RIASEC match (weight = 70%)
        for i, trait in enumerate(top_traits):
            if trait in rule_riasec:
                pos_weight = (3 - i) * 15 # 45 for top 1, 30 for top 2, 15 for top 3
                if rule_riasec[0] == trait:
                    pos_weight += 25
                score += pos_weight

        # MBTI match (weight = 30%)
        if mbti_type in rule_mbti:
            score += 30
        else:
            # Partial MBTI match
            mbti_matches = sum(1 for char in mbti_type if any(char in target_mbti for target_mbti in rule_mbti))
            score += mbti_matches * 5

        career_info = careers_data.get(career_name, {
            "mo_ta": "Môi trường làm việc chuyên nghiệp, cơ hội phát triển cao.",
            "ky_nang": "Kỹ năng chuyên môn, giao tiếp và làm việc nhóm.",
            "muc_luong": "Thỏa thuận theo năng lực.",
            "trien_vong": "Tiềm năng phát triển ổn định."
        })

        recommended_careers.append({
            "ten_nganh": career_name.title(),
            "score": score,
            "mo_ta": career_info.get("mo_ta"),
            "ky_nang": career_info.get("ky_nang"),
            "muc_luong": career_info.get("muc_luong"),
            "trien_vong": career_info.get("trien_vong")
        })

    # Sort careers by match score descending
    recommended_careers.sort(key=lambda x: x["score"], reverse=True)

    # Top Major Groups (Nhóm ngành chính)
    top_major_groups = [MAJOR_GROUPS[t] for t in top_traits]

    return {
        "holland_code": holland_code,
        "mbti_type": mbti_type,
        "riasec_scores": riasec_scores,
        "mbti_poles": mbti_poles,
        "top_major_groups": top_major_groups,
        "recommended_careers": recommended_careers[:5]
    }

# -----------------------------------------------------------------------------
# STREAMLIT UI IMPLEMENTATION (CLEAN WHITE THEME)
# -----------------------------------------------------------------------------
def run_streamlit_app():
    import streamlit as st

    # Page config
    st.set_page_config(
        page_title="Tư Vấn Hướng Nghiệp Rule-Based",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom White Theme CSS Injection
    st.markdown("""
        <style>
            /* Global Light / White Styling */
            .stApp {
                background-color: #ffffff;
                color: #1f2937;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            }

            /* Header Section */
            .main-header {
                background: linear-gradient(135deg, #ffffff 0%, #f3f4f6 100%);
                padding: 24px;
                border-radius: 12px;
                border: 1px solid #e5e7eb;
                margin-bottom: 24px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.02);
            }

            .main-title {
                color: #1e3a8a;
                font-size: 28px;
                font-weight: 700;
                margin-bottom: 8px;
            }

            .main-subtitle {
                color: #4b5563;
                font-size: 15px;
            }

            /* Quiz Question Card */
            .q-card {
                background-color: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 10px;
                padding: 16px 20px;
                margin-bottom: 14px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.03);
            }

            .q-number {
                display: inline-block;
                background-color: #eff6ff;
                color: #2563eb;
                font-weight: 600;
                padding: 3px 8px;
                border-radius: 6px;
                font-size: 13px;
                margin-bottom: 8px;
            }

            .q-text {
                font-size: 16px;
                font-weight: 500;
                color: #111827;
                margin-bottom: 10px;
            }

            /* Result Card */
            .result-card {
                background-color: #ffffff;
                border: 1px solid #d1d5db;
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 16px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            }

            .result-badge {
                display: inline-block;
                background-color: #2563eb;
                color: #ffffff;
                font-weight: 700;
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 18px;
                letter-spacing: 1px;
            }

            .career-title {
                color: #1d4ed8;
                font-size: 20px;
                font-weight: 700;
                margin-bottom: 8px;
            }

            .career-desc {
                color: #374151;
                font-size: 14px;
                line-height: 1.6;
            }

            .tag-box {
                background-color: #f3f4f6;
                color: #1f2937;
                padding: 4px 10px;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
                margin-right: 6px;
            }

            /* Customizing Streamlit Controls */
            .stRadio > label {
                font-weight: 500;
                color: #374151;
            }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
        <div class="main-header">
            <div class="main-title">🎯 Đánh Giá Hướng Nghiệp Rule-Based (Cấp Độ 1)</div>
            <div class="main-subtitle">Hệ thống phân tích tính cách (MBTI) & sở thích nghề nghiệp (RIASEC) để gợi ý nhóm ngành phù hợp.</div>
        </div>
    """, unsafe_allow_html=True)

    # Load questions data
    data = load_questions()
    questions = data.get("questions", [])
    scale_labels = {item["value"]: f"{item['value']} - {item['label']}" for item in data["scale"]["labels"]}

    # Sidebar Options
    st.sidebar.title("⚙️ Tùy chọn")
    st.sidebar.info("💡 Trả lời 40 câu hỏi trắc nghiệm bên dưới theo mức độ phù hợp với bản thân (từ 1 đến 5).")
    
    # Initialize answers in session_state
    if "answers" not in st.session_state:
        st.session_state.answers = {q["id"]: 3 for q in questions}

    # Tabs for RIASEC & MBTI
    tab1, tab2 = st.tabs(["📝 Phân 1: Sở Thích Nghề Nghiệp (RIASEC)", "🧠 Phần 2: Phong Cách Cá Nhân (MBTI)"])

    riasec_qs = [q for q in questions if q.get("section") == "riasec"]
    mbti_qs = [q for q in questions if q.get("section") == "mbti"]

    with tab1:
        st.subheader("📌 Chọn mức độ phù hợp (1: Hoàn toàn không đúng ➔ 5: Hoàn toàn đúng)")
        for q in riasec_qs:
            q_id = q["id"]
            st.markdown(f"""
                <div class="q-card">
                    <span class="q-number">Câu {q['order']}/40 • Nhóm {q['trait']}</span>
                    <div class="q-text">{q['text']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.session_state.answers[q_id] = st.radio(
                f"Lựa chọn cho câu {q['order']}:",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: scale_labels[x],
                index=st.session_state.answers[q_id] - 1,
                key=f"radio_{q_id}",
                horizontal=True,
                label_visibility="collapsed"
            )

    with tab2:
        st.subheader("📌 Chọn mức độ phù hợp với tính cách của bạn")
        for q in mbti_qs:
            q_id = q["id"]
            st.markdown(f"""
                <div class="q-card">
                    <span class="q-number">Câu {q['order']}/40 • Chiều {q['dimension']} ({q['pole']})</span>
                    <div class="q-text">{q['text']}</div>
                </div>
            """, unsafe_allow_html=True)

            st.session_state.answers[q_id] = st.radio(
                f"Lựa chọn cho câu {q['order']}:",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: scale_labels[x],
                index=st.session_state.answers[q_id] - 1,
                key=f"radio_{q_id}",
                horizontal=True,
                label_visibility="collapsed"
            )

    st.markdown("---")
    
    # Submit / Calculate Button
    col_btn1, col_btn2, _ = st.columns([2, 2, 4])
    with col_btn1:
        analyze_btn = st.button("🚀 Phân Tích & Xem Kết Quả", type="primary", use_container_width=True)
    with col_btn2:
        if st.button("🔄 Đặt Lại Tất Cả", use_container_width=True):
            st.session_state.answers = {q["id"]: 3 for q in questions}
            st.rerun()

    if analyze_btn or "analysis_result" in st.session_state:
        results = evaluate_assessment(st.session_state.answers)
        st.session_state.analysis_result = results

        st.markdown("## 📊 KẾT QUẢ ĐÁNH GIÁ VÀ GỢI Ý NGHỀ NGHIỆP")

        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown(f"""
                <div class="result-card">
                    <h3>📌 Holland Code (RIASEC)</h3>
                    <div class="result-badge">{results['holland_code']}</div>
                    <p style="margin-top: 12px; color: #4b5563;">3 Nhóm sở thích nổi trội nhất của bạn dựa trên 24 câu hỏi RIASEC.</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Show RIASEC Score Progress Bars
            st.write("**Chi tiết điểm các nhóm RIASEC:**")
            for trait, score in results["riasec_scores"].items():
                pct = int((score / 20) * 100)
                st.write(f"**{trait}** - {TRAIT_NAMES[trait]}: **{score}/20** ({pct}%)")
                st.progress(pct / 100)

        with col2:
            st.markdown(f"""
                <div class="result-card">
                    <h3>📌 Loại Tính Cách (MBTI)</h3>
                    <div class="result-badge" style="background-color: #059669;">{results['mbti_type']}</div>
                    <p style="margin-top: 12px; color: #4b5563;">Phong cách cá nhân và môi trường làm việc phù hợp.</p>
                </div>
            """, unsafe_allow_html=True)

            # Show MBTI breakdown
            st.write("**Chi tiết các chiều tính cách MBTI:**")
            poles = results["mbti_poles"]
            st.write(f"- **E / I** (Hướng ngoại / Hướng nội): {poles['E']} vs {poles['I']}")
            st.write(f"- **S / N** (Thực tế / Trực giác): {poles['S']} vs {poles['N']}")
            st.write(f"- **T / F** (Lý trí / Cảm xúc): {poles['T']} vs {poles['F']}")
            st.write(f"- **J / P** (Nguyên tắc / Linh hoạt): {poles['J']} vs {poles['P']}")

        st.markdown("---")
        st.markdown("### 🎯 TOP NHÓM NGÀNH & NGHỀ NGHIỆP PHÙ HỢP NHẤT")

        # Display Major Groups
        st.markdown("#### 🏛️ Nhóm Ngành Đại Học / Cao Đẳng Khuyên Dùng:")
        for mg in results["top_major_groups"]:
            st.markdown(f"- **{mg}**")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 💼 Danh Sách Ngành Nghề Gợi Ý Chi Tiết:")

        for i, c in enumerate(results["recommended_careers"], 1):
            st.markdown(f"""
                <div class="result-card">
                    <div class="career-title">#{i}. {c['ten_nganh']}</div>
                    <div class="career-desc"><b>📝 Mô tả:</b> {c['mo_ta']}</div>
                    <div class="career-desc" style="margin-top:6px;"><b>💡 Kỹ năng cần có:</b> {c['ky_nang']}</div>
                    <div style="margin-top: 10px;">
                        <span class="tag-box">💰 Mức lương: {c['muc_luong']}</span>
                        <span class="tag-box" style="background-color:#e0f2fe; color:#0369a1;">📈 Triển vọng: {c['trien_vong']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# ENTRY POINT & RUNNER LOGIC
# -----------------------------------------------------------------------------
def run_cli_demo():
    print("=" * 60)
    print("=== DEMO CẤP ĐỘ 1: RULE-BASED CAREER ADVISOR ===")
    print("=" * 60)

    # Test sample input (All answers = 4)
    sample_answers = {f"R0{i}": 4 for i in range(1, 5)}
    sample_answers.update({f"I0{i}": 4 for i in range(1, 5)})
    sample_answers.update({f"A0{i}": 4 for i in range(1, 5)})
    sample_answers.update({f"S0{i}": 4 for i in range(1, 5)})
    sample_answers.update({f"E0{i}": 4 for i in range(1, 5)})
    sample_answers.update({f"C0{i}": 4 for i in range(1, 5)})
    
    sample_answers.update({"EI01": 4, "EI02": 4, "EI03": 2, "EI04": 2})
    sample_answers.update({"SN01": 2, "SN02": 2, "SN03": 5, "SN04": 5})
    sample_answers.update({"TF01": 2, "TF02": 2, "TF03": 5, "TF04": 5})
    sample_answers.update({"JP01": 2, "JP02": 2, "JP03": 4, "JP04": 4})

    res = evaluate_assessment(sample_answers)

    print("\n--- TEST KẾT QUẢ ĐÁNH GIÁ CHẨN MẪU (Sample Input: High S/A/E, INFP) ---")
    print(f"📌 Holland Code: {res['holland_code']}")
    print(f"📌 MBTI Type: {res['mbti_type']}")
    print(f"🎯 Nhóm ngành chính: {', '.join(res['top_major_groups'])}")
    top_jobs = [c['ten_nganh'] for c in res['recommended_careers']]
    print(f"💼 Ngành gợi ý: {', '.join(top_jobs)}")
    print("-" * 60)

if __name__ == "__main__":
    # Check if running via streamlit
    is_streamlit = False
    try:
        import streamlit as st
        # If running via `streamlit run`, streamlit sets internal flags
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx() is not None:
            is_streamlit = True
    except ImportError:
        pass

    if is_streamlit:
        run_streamlit_app()
    else:
        run_cli_demo()
        print("\n🚀 Đang khởi chạy giao diện Web Streamlit (Tông màu trắng)...")
        
        # Check venv python path
        venv_python = os.path.join(BASE_DIR, ".venv", "bin", "python")
        if os.path.exists(venv_python):
            cmd = [venv_python, "-m", "streamlit", "run", __file__]
        else:
            cmd = ["streamlit", "run", __file__]

        try:
            subprocess.run(cmd)
        except KeyboardInterrupt:
            print("\n👋 Đã dừng ứng dụng Web Streamlit.")
