"""
🚀 FASTAPI WEB APP - TƯ VẤN ĐỊNH HƯỚNG SỰ NGHIỆP CẢ NGHỆ VÀ TRÍ TUỆ NHÂN TẠO
Tích hợp 4 Cấp độ AI:
1. Rule-Based (Hệ thống dựa trên luật)
2. LLM Chatbot (OpenAI)
3. Reactive Agent (OpenAI + Tools)
4. Autonomous Agent (OpenAI + Planning & Memory)
"""

import os
import sys
import json
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Thêm thư mục hiện tại và src vào sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Import các cấp độ AI
from src.ai_levels.level1_rule_based import evaluate_assessment, load_questions
from src.ai_levels.level2_llm_chatbot import llm_chatbot
from src.ai_levels.level3_reactive_agent import reactive_agent_loop
from src.ai_levels.level4_autonomous_agent import AutonomousGoalAgent
from src.providers import OpenAIProvider

app = FastAPI(
    title="Hệ Thống Tư Vấn Hướng Nghiệp AI (Cấp Độ 1 -> 4)",
    description="Ứng dụng FastAPI tích hợp Rule-based, OpenAI LLM Chatbot, Reactive Agent & Autonomous Agent",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------
# PYDANTIC MODELS FOR API REQUESTS
# -----------------------------------------------------------------------------
class RulebaseRequest(BaseModel):
    answers: Dict[str, int]

class ChatbotRequest(BaseModel):
    message: str

class ReactiveAgentRequest(BaseModel):
    message: str

class AutonomousAgentRequest(BaseModel):
    goal: str
    max_steps: Optional[int] = 5


# -----------------------------------------------------------------------------
# API ENDPOINTS
# -----------------------------------------------------------------------------
@app.get("/api/questions")
def get_questions_api():
    """Lấy danh sách câu hỏi trắc nghiệm RIASEC + MBTI từ config/question.json"""
    try:
        data = load_questions()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/rulebase/evaluate")
def evaluate_rulebase_api(req: RulebaseRequest):
    """Tính toán kết quả Rule-based từ câu trả lời trắc nghiệm"""
    try:
        result = evaluate_assessment(req.answers)
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chatbot")
def chatbot_api(req: ChatbotRequest):
    """Gọi Cấp độ 2: LLM Chatbot sử dụng OpenAI"""
    try:
        provider = OpenAIProvider()
        response_text = llm_chatbot(req.message, provider=provider)
        return {"success": True, "response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/agent/reactive")
def reactive_agent_api(req: ReactiveAgentRequest):
    """Gọi Cấp độ 3: Reactive Agent (OpenAI + Tools)"""
    try:
        provider = OpenAIProvider()
        result = reactive_agent_loop(
            user_query=req.message,
            provider=provider,
            verbose=False,
            return_details=True
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/agent/autonomous")
def autonomous_agent_api(req: AutonomousAgentRequest):
    """Gọi Cấp độ 4: Autonomous Agent (OpenAI + Planning & Memory)"""
    try:
        provider = OpenAIProvider()
        agent = AutonomousGoalAgent(
            goal=req.goal,
            max_steps=req.max_steps or 5,
            provider=provider
        )
        result = agent.execute(verbose=False)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------------------------------------------------
# WEB INTERFACE (HTML + JS + MODERN CLEAN STYLING)
# -----------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def index_page():
    html_content = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hệ Thống Tư Vấn Hướng Nghiệp AI</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #2563eb;
            --primary-hover: #1d4ed8;
            --bg-main: #f8fafc;
            --card-bg: #ffffff;
            --text-dark: #0f172a;
            --text-muted: #64748b;
            --border-color: #e2e8f0;
            --accent-green: #10b981;
            --accent-purple: #8b5cf6;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        body {
            background-color: var(--bg-main);
            color: var(--text-dark);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        header {
            background: #ffffff;
            border-bottom: 1px solid var(--border-color);
            padding: 18px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .logo-area {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo-icon {
            background: linear-gradient(135deg, #2563eb, #8b5cf6);
            color: #fff;
            width: 40px;
            height: 40px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            font-weight: 700;
        }

        .logo-title {
            font-size: 20px;
            font-weight: 700;
            color: var(--text-dark);
        }

        .logo-subtitle {
            font-size: 12px;
            color: var(--text-muted);
        }

        .nav-tabs {
            display: flex;
            gap: 8px;
            background: #f1f5f9;
            padding: 6px;
            border-radius: 12px;
        }

        .tab-btn {
            border: none;
            background: transparent;
            padding: 10px 18px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            color: var(--text-muted);
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .tab-btn.active {
            background: #ffffff;
            color: var(--primary);
            box-shadow: 0 2px 4px rgba(0,0,0,0.06);
        }

        .container {
            max-width: 1200px;
            margin: 30px auto;
            padding: 0 20px;
            width: 100%;
            flex: 1;
        }

        .tab-content {
            display: none;
            animation: fadeIn 0.3s ease-in-out;
        }

        .tab-content.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* CARD STYLES */
        .card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 28px;
            margin-bottom: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        }

        .card-header {
            margin-bottom: 20px;
        }

        .card-title {
            font-size: 22px;
            font-weight: 700;
            color: var(--text-dark);
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .card-desc {
            font-size: 14px;
            color: var(--text-muted);
            line-height: 1.5;
        }

        /* RULEBASE QUIZ UI */
        .quiz-section-title {
            font-size: 16px;
            font-weight: 700;
            margin: 20px 0 12px 0;
            color: var(--primary);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .question-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 12px;
        }

        .question-meta {
            font-size: 12px;
            font-weight: 600;
            color: var(--primary);
            background: #eff6ff;
            padding: 2px 8px;
            border-radius: 6px;
            display: inline-block;
            margin-bottom: 6px;
        }

        .question-text {
            font-size: 15px;
            font-weight: 500;
            margin-bottom: 12px;
        }

        .scale-options {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }

        .scale-option {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 13px;
            color: #334155;
            cursor: pointer;
            background: #fff;
            padding: 6px 14px;
            border-radius: 8px;
            border: 1px solid #cbd5e1;
            transition: all 0.15s ease;
        }

        .scale-option:hover {
            border-color: var(--primary);
            background: #f0f7ff;
        }

        .btn-primary {
            background: var(--primary);
            color: #fff;
            border: none;
            padding: 12px 24px;
            border-radius: 10px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .btn-primary:hover {
            background: var(--primary-hover);
        }

        .btn-secondary {
            background: #e2e8f0;
            color: #334155;
            border: none;
            padding: 12px 24px;
            border-radius: 10px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            margin-left: 10px;
        }

        /* CHAT UI */
        .chat-box {
            background: #f8fafc;
            border: 1px solid var(--border-color);
            border-radius: 12px;
            height: 450px;
            overflow-y: auto;
            padding: 20px;
            margin-bottom: 16px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .chat-msg {
            max-width: 80%;
            padding: 14px 18px;
            border-radius: 14px;
            font-size: 14px;
            line-height: 1.6;
        }

        .chat-msg.user {
            align-self: flex-end;
            background: var(--primary);
            color: #ffffff;
            border-bottom-right-radius: 2px;
        }

        .chat-msg.bot {
            align-self: flex-start;
            background: #ffffff;
            color: var(--text-dark);
            border: 1px solid var(--border-color);
            border-bottom-left-radius: 2px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        }

        .chat-input-group {
            display: flex;
            gap: 10px;
        }

        .chat-input {
            flex: 1;
            padding: 14px 18px;
            border: 1px solid var(--border-color);
            border-radius: 12px;
            font-size: 15px;
            outline: none;
            background: #fff;
        }

        .chat-input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(37,99,235,0.1);
        }

        /* AGENT STEP TRACE */
        .step-trace {
            background: #f1f5f9;
            border-left: 4px solid var(--primary);
            padding: 12px 16px;
            border-radius: 6px;
            margin-bottom: 10px;
            font-size: 13px;
        }

        .step-pill {
            display: inline-block;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
            margin-bottom: 6px;
            text-transform: uppercase;
        }

        .pill-thought { background: #dbeafe; color: #1e40af; }
        .pill-action { background: #fef3c7; color: #92400e; }
        .pill-observation { background: #d1fae5; color: #065f46; }

        /* RESULT GRID */
        .result-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 20px;
        }

        .badge-box {
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            color: #fff;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 18px;
            font-weight: 700;
            display: inline-block;
            margin-top: 8px;
        }

        .career-card {
            background: #ffffff;
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 14px;
        }

        .career-name {
            font-size: 18px;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 6px;
        }

        .tag {
            display: inline-block;
            background: #eff6ff;
            color: #1e40af;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            margin-right: 6px;
            margin-top: 6px;
        }

        footer {
            text-align: center;
            padding: 20px;
            color: var(--text-muted);
            font-size: 13px;
            border-top: 1px solid var(--border-color);
            background: #fff;
        }
    </style>
</head>
<body>

    <header>
        <div class="logo-area">
            <div class="logo-icon">🎯</div>
            <div>
                <div class="logo-title">Career AI Advisor</div>
                <div class="logo-subtitle">Hệ Thống Tư Vấn Hướng Nghiệp Đa Cấp Độ AI</div>
            </div>
        </div>
        <div class="nav-tabs">
            <button class="tab-btn active" onclick="switchTab('rulebase')">
                <span>🎯 Cấp 1: Rule-Based</span>
            </button>
            <button class="tab-btn" onclick="switchTab('chatbot')">
                <span>💬 Cấp 2: LLM Chatbot</span>
            </button>
            <button class="tab-btn" onclick="switchTab('reactive')">
                <span>🤖 Cấp 3: Reactive Agent</span>
            </button>
            <button class="tab-btn" onclick="switchTab('autonomous')">
                <span>🚀 Cấp 4: Autonomous Agent</span>
            </button>
        </div>
    </header>

    <div class="container">
        
        <!-- TAB 1: RULE BASE -->
        <div id="tab-rulebase" class="tab-content active">
            <div class="card">
                <div class="card-header">
                    <div class="card-title">🎯 Cấp Độ 1: Rule-Based Assessment</div>
                    <div class="card-desc">Đánh giá sở thích nghề nghiệp (RIASEC) & phong cách cá nhân (MBTI) dựa trên luật cố định. Trả lời các câu hỏi bên dưới từ 1 (Hoàn toàn không đúng) đến 5 (Hoàn toàn đúng).</div>
                </div>

                <div id="quiz-container">
                    <p style="color: var(--text-muted);">Đang tải bộ câu hỏi trắc nghiệm...</p>
                </div>

                <div style="margin-top: 24px;">
                    <button class="btn-primary" onclick="submitRulebase()">🚀 Phân Tích & Cho Kết Quả</button>
                    <button class="btn-secondary" onclick="resetRulebase()">🔄 Làm Lại</button>
                </div>

                <div id="rulebase-result" style="margin-top: 30px; display: none;"></div>
            </div>
        </div>

        <!-- TAB 2: LLM CHATBOT -->
        <div id="tab-chatbot" class="tab-content">
            <div class="card">
                <div class="card-header">
                    <div class="card-title">💬 Cấp Độ 2: Baseline LLM Chatbot (OpenAI)</div>
                    <div class="card-desc">Hội thoại tự nhiên cùng OpenAI LLM (gpt-4o-mini). Chatbot giải đáp dựa trên tri thức chung nhưng KHÔNG có công cụ tra cứu dữ liệu thời gian thực.</div>
                </div>

                <div class="chat-box" id="chatbot-box">
                    <div class="chat-msg bot">
                        👋 Xin chào! Tôi là LLM Chatbot tư vấn hướng nghiệp. Bạn có thắc mắc gì về các nhóm ngành học hoặc định hướng nghề nghiệp không?
                    </div>
                </div>

                <div class="chat-input-group">
                    <input type="text" id="chatbot-input" class="chat-input" placeholder="Nhập câu hỏi tư vấn... (Ấn Enter hoặc nhấn Gửi)" onkeypress="if(event.key==='Enter') sendChatbot()">
                    <button class="btn-primary" onclick="sendChatbot()">Gửi</button>
                </div>
            </div>
        </div>

        <!-- TAB 3: REACTIVE AGENT -->
        <div id="tab-reactive" class="tab-content">
            <div class="card">
                <div class="card-header">
                    <div class="card-title">🤖 Cấp Độ 3: Reactive ReAct Agent (OpenAI + Tools)</div>
                    <div class="card-desc">Agent thông minh tự thực hiện vòng lặp suy luận (Thought -> Action -> Observation) và gọi các công cụ thực tế (tra cứu khối thi, ngành nghề, học phí trường ĐH).</div>
                </div>

                <div class="chat-box" id="reactive-box">
                    <div class="chat-msg bot">
                        🧠 Chào bạn! Tôi là Reactive Agent trang bị công cụ tra cứu thông tin trường học, ngành nghề và khối thi. Hãy đặt câu hỏi cho tôi! (Ví dụ: "Em học khối A00, tư vấn ngành CNTT và các trường học phí dưới 50tr ở Miền Bắc")
                    </div>
                </div>

                <div class="chat-input-group">
                    <input type="text" id="reactive-input" class="chat-input" placeholder="Hỏi ReAct Agent... (Ấn Enter hoặc nhấn Gửi)" onkeypress="if(event.key==='Enter') sendReactive()">
                    <button class="btn-primary" onclick="sendReactive()">Gửi Câu Hỏi</button>
                </div>
            </div>
        </div>

        <!-- TAB 4: AUTONOMOUS AGENT -->
        <div id="tab-autonomous" class="tab-content">
            <div class="card">
                <div class="card-header">
                    <div class="card-title">🚀 Cấp Độ 4: Autonomous Goal Agent (OpenAI + Planning & Memory)</div>
                    <div class="card-desc">Agent tự chủ cao cấp: Tự phân rã Mục Tiêu lớn thành kế hoạch từng bước, tự thực thi công cụ, duy trì Bộ Nhớ (Memory) và lập báo cáo định hướng toàn diện.</div>
                </div>

                <div style="margin-bottom: 20px;">
                    <label style="font-weight: 600; font-size: 14px; display: block; margin-bottom: 8px;">Nhập Mục Tiêu Phức Tạp Của Học Sinh:</label>
                    <input type="text" id="autonomous-goal-input" class="chat-input" style="width: 100%; margin-bottom: 12px;" value="Lên kế hoạch tư vấn cho học sinh thi khối A00, tìm hiểu kỹ năng ngành Công nghệ thông tin và tìm trường học phí dưới 40 triệu ở Miền Bắc.">
                    <button class="btn-primary" onclick="runAutonomousAgent()">🚀 Lập Kế Hoạch & Thực Thi Tự Chủ</button>
                </div>

                <div id="autonomous-result" style="display: none;"></div>
            </div>
        </div>

    </div>

    <footer>
        FastAPI Career Advisor • Tích hợp OpenAI GPT Models & ReAct Agent Architecture
    </footer>

    <script>
        let quizData = null;
        let answersState = {};

        function switchTab(tabId) {
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

            event.currentTarget.classList.add('active');
            document.getElementById('tab-' + tabId).classList.add('active');
        }

        // LOAD QUIZ FOR RULEBASE
        async function loadQuiz() {
            try {
                const res = await fetch('/api/questions');
                quizData = await res.json();
                renderQuiz();
            } catch(e) {
                document.getElementById('quiz-container').innerHTML = '<p style="color:red;">Lỗi tải câu hỏi: ' + e.message + '</p>';
            }
        }

        function renderQuiz() {
            if (!quizData || !quizData.questions) return;
            const container = document.getElementById('quiz-container');
            let html = '';

            const riasecQs = quizData.questions.filter(q => q.section === 'riasec');
            const mbtiQs = quizData.questions.filter(q => q.section === 'mbti');

            html += `<div class="quiz-section-title">📌 Phần 1: Sở Thích Nghề Nghiệp (RIASEC - ${riasecQs.length} câu)</div>`;
            riasecQs.forEach(q => {
                answersState[q.id] = 3;
                html += renderQuestionCard(q);
            });

            html += `<div class="quiz-section-title" style="margin-top: 30px;">🧠 Phần 2: Phong Cách Cá Nhân (MBTI - ${mbtiQs.length} câu)</div>`;
            mbtiQs.forEach(q => {
                answersState[q.id] = 3;
                html += renderQuestionCard(q);
            });

            container.innerHTML = html;
        }

        function renderQuestionCard(q) {
            return `
                <div class="question-card">
                    <span class="question-meta">Câu ${q.order} • ${q.section.toUpperCase()} (${q.trait || q.pole})</span>
                    <div class="question-text">${q.text}</div>
                    <div class="scale-options">
                        ${[1,2,3,4,5].map(v => `
                            <label class="scale-option">
                                <input type="radio" name="q_${q.id}" value="${v}" ${v===3?'checked':''} onchange="answersState['${q.id}']=${v}">
                                ${v} - ${v===1?'Rất sai':v===3?'Trung lập':v===5?'Rất đúng':''}
                            </label>
                        `).join('')}
                    </div>
                </div>
            `;
        }

        async function submitRulebase() {
            const resDiv = document.getElementById('rulebase-result');
            resDiv.style.display = 'block';
            resDiv.innerHTML = '<p style="color: var(--primary);">⏳ Đang phân tích kết quả...</p>';

            try {
                const response = await fetch('/api/rulebase/evaluate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({answers: answersState})
                });
                const data = await response.json();
                if(data.success) {
                    const r = data.result;
                    let html = `
                        <div class="result-grid">
                            <div style="background:#f8fafc; padding:20px; border-radius:12px; border:1px solid #e2e8f0;">
                                <h3>📌 Holland Code (RIASEC)</h3>
                                <div class="badge-box">${r.holland_code}</div>
                                <p style="margin-top:10px; font-size:13px; color:#64748b;">Nhóm ngành gợi ý:</p>
                                <ul>${r.top_major_groups.map(g=>`<li style="font-size:13px; font-weight:600; margin-top:4px;">${g}</li>`).join('')}</ul>
                            </div>
                            <div style="background:#f8fafc; padding:20px; border-radius:12px; border:1px solid #e2e8f0;">
                                <h3>📌 Loại Tính Cách (MBTI)</h3>
                                <div class="badge-box" style="background:linear-gradient(135deg, #10b981, #059669);">${r.mbti_type}</div>
                                <p style="margin-top:10px; font-size:13px; color:#64748b;">Chi tiết điểm số:</p>
                                <div style="font-size:13px; font-weight:500;">
                                    E/I: ${r.mbti_poles.E} vs ${r.mbti_poles.I} | S/N: ${r.mbti_poles.S} vs ${r.mbti_poles.N}<br>
                                    T/F: ${r.mbti_poles.T} vs ${r.mbti_poles.F} | J/P: ${r.mbti_poles.J} vs ${r.mbti_poles.P}
                                </div>
                            </div>
                        </div>

                        <h3 style="margin-top: 24px; margin-bottom: 12px;">💼 Danh Sách Ngành Nghề Gợi Ý Chi Tiết:</h3>
                    `;

                    r.recommended_careers.forEach((c, idx) => {
                        html += `
                            <div class="career-card">
                                <div class="career-name">#${idx+1}. ${c.ten_nganh}</div>
                                <p style="font-size:14px; color:#334155; margin-bottom:6px;"><b>Mô tả:</b> ${c.mo_ta}</p>
                                <p style="font-size:14px; color:#334155;"><b>Kỹ năng:</b> ${c.ky_nang}</p>
                                <div>
                                    <span class="tag">💰 Lương: ${c.muc_luong}</span>
                                    <span class="tag" style="background:#ecfdf5; color:#047857;">📈 Triển vọng: ${c.trien_vong}</span>
                                </div>
                            </div>
                        `;
                    });

                    resDiv.innerHTML = html;
                }
            } catch(e) {
                resDiv.innerHTML = '<p style="color:red;">Lỗi phân tích: ' + e.message + '</p>';
            }
        }

        function resetRulebase() {
            renderQuiz();
            document.getElementById('rulebase-result').style.display = 'none';
        }

        // CHATBOT (LEVEL 2)
        async function sendChatbot() {
            const input = document.getElementById('chatbot-input');
            const msg = input.value.trim();
            if(!msg) return;

            const box = document.getElementById('chatbot-box');
            box.innerHTML += `<div class="chat-msg user">${msg}</div>`;
            input.value = '';
            box.scrollTop = box.scrollHeight;

            const loadingId = 'loading-' + Date.now();
            box.innerHTML += `<div class="chat-msg bot" id="${loadingId}">⏳ Chatbot đang suy nghĩ...</div>`;
            box.scrollTop = box.scrollHeight;

            try {
                const res = await fetch('/api/chatbot', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: msg})
                });
                const data = await res.json();
                document.getElementById(loadingId).innerText = data.response;
            } catch(e) {
                document.getElementById(loadingId).innerText = '❌ Lỗi kết nối Chatbot: ' + e.message;
            }
            box.scrollTop = box.scrollHeight;
        }

        // REACTIVE AGENT (LEVEL 3)
        async function sendReactive() {
            const input = document.getElementById('reactive-input');
            const msg = input.value.trim();
            if(!msg) return;

            const box = document.getElementById('reactive-box');
            box.innerHTML += `<div class="chat-msg user">${msg}</div>`;
            input.value = '';
            box.scrollTop = box.scrollHeight;

            const loadingId = 'loading-' + Date.now();
            box.innerHTML += `<div class="chat-msg bot" id="${loadingId}">🧠 ReAct Agent đang gọi công cụ & suy luận...</div>`;
            box.scrollTop = box.scrollHeight;

            try {
                const res = await fetch('/api/agent/reactive', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: msg})
                });
                const data = await res.json();

                let traceHtml = '';
                if(data.steps && data.steps.length > 0) {
                    traceHtml += '<div style="margin-bottom: 12px; font-size:12px; font-weight:700; color:#475569;">🔄 VÒNG LẶP SUY LUẬN (REACT TRACE):</div>';
                    data.steps.forEach(st => {
                        traceHtml += `
                            <div class="step-trace">
                                <div><span class="step-pill pill-thought">Step ${st.step} Thought</span> ${st.thought}</div>
                                ${st.action !== 'Final Answer' ? `<div><span class="step-pill pill-action">Action</span> ${st.action}</div>` : ''}
                                <div><span class="step-pill pill-observation">Observation</span> ${st.observation}</div>
                            </div>
                        `;
                    });
                }

                document.getElementById(loadingId).innerHTML = traceHtml + `<div style="font-size:15px; font-weight:600; color:#0f172a; margin-top:8px;">✅ Final Answer:</div>` + data.final_answer.replace(/\\n/g, '<br>');
            } catch(e) {
                document.getElementById(loadingId).innerText = '❌ Lỗi Agent: ' + e.message;
            }
            box.scrollTop = box.scrollHeight;
        }

        // AUTONOMOUS AGENT (LEVEL 4)
        async function runAutonomousAgent() {
            const goal = document.getElementById('autonomous-goal-input').value.trim();
            if(!goal) return;

            const resDiv = document.getElementById('autonomous-result');
            resDiv.style.display = 'block';
            resDiv.innerHTML = '<p style="color: var(--primary);">🚀 Agent đang tự chủ lập kế hoạch, gọi tools và duy trì bộ nhớ...</p>';

            try {
                const res = await fetch('/api/agent/autonomous', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({goal: goal, max_steps: 5})
                });
                const data = await res.json();

                let html = `<h3 style="margin-bottom:12px;">🎯 Goal: ${data.goal}</h3>`;

                if(data.memory && data.memory.length > 0) {
                    html += `<div style="font-size:14px; font-weight:700; margin-bottom:10px;">📋 Vết Bộ Nhớ (Memory Trace):</div>`;
                    data.memory.forEach(m => {
                        html += `
                            <div class="step-trace" style="border-left-color: var(--accent-purple);">
                                <div><b>Step ${m.step} Plan:</b> ${m.plan}</div>
                                <div><b>Action:</b> <code>${m.action}</code></div>
                                <div><b>Observation/Result:</b> ${m.result}</div>
                            </div>
                        `;
                    });
                }

                html += `
                    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:12px; padding:20px; margin-top:16px;">
                        <h3 style="color: var(--primary); margin-bottom:10px;">📝 Báo Cáo Định Hướng Hoàn Chỉnh:</h3>
                        <div style="font-size:15px; line-height:1.6; white-space: pre-line;">${data.final_summary}</div>
                    </div>
                `;

                resDiv.innerHTML = html;
            } catch(e) {
                resDiv.innerHTML = '<p style="color:red;">❌ Lỗi Autonomous Agent: ' + e.message + '</p>';
            }
        }

        // Initialize quiz on load
        window.onload = loadQuiz;
    </script>
</body>
</html>
"""
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    import uvicorn
    print("==================================================")
    print("🚀 ĐANG KHỞI CHẠY FASTAPI APP TẠI http://127.0.0.1:8000")
    print("==================================================")
    uvicorn.run(app, host="127.0.0.1", port=8000)
