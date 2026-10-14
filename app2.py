"""
Banque Misr – AI Chat Assistant
Streamlit app — deploy to Streamlit Cloud

Requirements (requirements.txt):
    streamlit
    requests
"""

import base64
import time
import requests
import streamlit as st
from pathlib import Path

# ─── CONFIG ────────────────────────────────────────────────────────────────────

FLOWISE_URL = "http://localhost:3000/api/v1/prediction/5570de1d-a438-4f08-928e-5732147b70f6"
# ↑ Replace with your public Flowise URL before deploying, e.g.:
# FLOWISE_URL = "https://cloud.flowiseai.com/api/v1/prediction/YOUR-ID-HERE"

# ─── PAGE SETUP ────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Banque Misr Assistant",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── LOGO AS BASE64 ────────────────────────────────────────────────────────────

def get_logo_b64():
    logo_path = Path(__file__).parent / "banque_misr_logo.png"
    if logo_path.exists():
        return base64.b64encode(logo_path.read_bytes()).decode()
    return None

logo_b64 = get_logo_b64()
logo_html = (
    f'<img src="data:image/png;base64,{logo_b64}" class="brand-logo" alt="Banque Misr"/>'
    if logo_b64
    else '<div class="brand-logo-placeholder">BM</div>'
)

# ─── CSS ───────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700&family=Cormorant+Garamond:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
    background-color: #f8f4f0 !important;
    color: #3a1a20;
    font-family: 'Cairo', sans-serif;
    font-weight: 400;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

/* Remove default padding */
.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
section[data-testid="stMain"] > div { padding: 0 !important; }

/* ── Page shell ── */
.page {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    max-width: 680px;
    margin: 0 auto;
    padding: 0 20px;
    position: relative;
}

/* ── Header ── */
.brand-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 0 28px;
    border-bottom: 2px solid rgba(134,47,64,0.18);
    margin-bottom: 28px;
    background: linear-gradient(180deg, #fff 0%, #f8f4f0 100%);
}
.brand-logo {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    object-fit: cover;
    margin-bottom: 18px;
    border: 2px solid rgba(134,47,64,0.3);
    box-shadow: 0 4px 20px rgba(134,47,64,0.12);
}
.brand-logo-placeholder {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    background: #862F40;
    border: 2px solid rgba(134,47,64,0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Cairo', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #E3A91B;
    margin-bottom: 18px;
}
.brand-name {
    font-family: 'Cairo', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: #862F40;
    text-transform: uppercase;
    line-height: 1;
}
.brand-line {
    width: 60px;
    height: 2px;
    background: linear-gradient(90deg, transparent, #E3A91B, transparent);
    margin: 10px auto;
}
.brand-sub {
    font-size: 0.72rem;
    letter-spacing: 0.3em;
    color: rgba(134,47,64,0.5);
    text-transform: uppercase;
}

/* ── Messages ── */
.messages-wrap {
    padding-bottom: 110px;
}

.msg-block {
    display: flex;
    margin-bottom: 20px;
    gap: 10px;
    align-items: flex-end;
}
.msg-block.user-block { flex-direction: row-reverse; }

.avatar-dot {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 700;
}
.avatar-dot.bot-av {
    background: #862F40;
    border: 1px solid rgba(134,47,64,0.4);
    color: #E3A91B;
}
.avatar-dot.user-av {
    background: #E3A91B;
    border: 1px solid rgba(227,169,27,0.4);
    color: #862F40;
}

.bubble {
    max-width: 80%;
    padding: 13px 17px;
    font-size: 0.92rem;
    line-height: 1.8;
    font-weight: 400;
    font-family: 'Cairo', sans-serif;
    unicode-bidi: plaintext;
    text-align: start;
}
.bot-bubble {
    background: #ffffff;
    border: 1px solid rgba(134,47,64,0.15);
    border-left: 3px solid #862F40;
    border-radius: 0 16px 16px 16px;
    color: #2a1015;
    box-shadow: 0 2px 8px rgba(134,47,64,0.06);
}
.user-bubble {
    background: #FBF1D9;
    border: 1px solid rgba(227,169,27,0.35);
    border-right: 3px solid #E3A91B;
    border-radius: 16px 0 16px 16px;
    color: #2a1015;
    text-align: start;
    margin-left: auto;
    box-shadow: 0 2px 8px rgba(227,169,27,0.08);
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 60px 20px 40px;
}
.empty-icon {
    font-size: 2.6rem;
    margin-bottom: 20px;
    opacity: 0.8;
}
.empty-title {
    font-family: 'Cairo', sans-serif;
    font-size: 1.4rem;
    font-weight: 600;
    color: #862F40;
    letter-spacing: 0.03em;
    margin-bottom: 10px;
}
.empty-desc {
    font-size: 0.85rem;
    color: rgba(134,47,64,0.5);
    line-height: 1.9;
    letter-spacing: 0.02em;
    max-width: 320px;
    margin: 0 auto;
}

/* ── Input box ── */
[data-testid="stChatInput"] {
    position: fixed !important;
    bottom: 0 !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: min(680px, 100%) !important;
    padding: 16px 20px 20px !important;
    background: linear-gradient(to top, #f8f4f0 75%, transparent) !important;
    z-index: 999 !important;
}
[data-testid="stChatInput"] textarea {
    background: #ffffff !important;
    border: 1px solid rgba(134,47,64,0.3) !important;
    border-radius: 14px !important;
    color: #2a1015 !important;
    font-family: 'Cairo', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 400 !important;
    caret-color: #862F40 !important;
    resize: none !important;
    unicode-bidi: plaintext !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: rgba(134,47,64,0.35) !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: rgba(134,47,64,0.55) !important;
    box-shadow: 0 0 0 3px rgba(134,47,64,0.08) !important;
    outline: none !important;
}
button[data-testid="stChatInputSubmitButton"] {
    background: #862F40 !important;
    border: 1px solid rgba(134,47,64,0.4) !important;
    border-radius: 10px !important;
    color: #E3A91B !important;
    transition: background 0.2s !important;
}
button[data-testid="stChatInputSubmitButton"]:hover {
    background: #6e2635 !important;
}
button[data-testid="stChatInputSubmitButton"] svg { fill: #E3A91B !important; }

/* ── Mobile tweaks ── */
@media (max-width: 480px) {
    .brand-logo { width: 85px; height: 85px; }
    .brand-name  { font-size: 1.4rem; }
    .bubble      { font-size: 0.87rem; }
    .page        { padding: 0 14px; }
}
</style>
""", unsafe_allow_html=True)


# ─── FLOWISE ───────────────────────────────────────────────────────────────────

def ask_flowise(question: str, session_id: str) -> str:
    try:
        resp = requests.post(
            FLOWISE_URL,
            json={"question": question, "overrideConfig": {"sessionId": session_id}},
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        return (
            data.get("text")
            or data.get("answer")
            or data.get("output")
            or data.get("response")
            or "عذراً، لم أفهم. ممكن تعيد السؤال؟ / Sorry, I didn't understand. Could you rephrase?"
        )
    except Exception:
        return "عذراً، حدث خطأ مؤقت. حاول مرة ثانية بعد لحظة 🙏 / A temporary error occurred. Please try again."


# ─── SESSION ───────────────────────────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = f"user-{int(time.time())}"


# ─── RENDER PAGE ───────────────────────────────────────────────────────────────

st.markdown('<div class="page">', unsafe_allow_html=True)

# Header
st.markdown(f"""
<div class="brand-header">
    {logo_html}
    <div class="brand-name">Banque Misr</div>
    <div class="brand-line"></div>
    <div class="brand-sub">Virtual Assistant</div>
</div>
""", unsafe_allow_html=True)

# Messages
st.markdown('<div class="messages-wrap">', unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🏦</div>
        <div class="empty-title">كيف يمكنني مساعدتك؟</div>
        <div class="empty-desc">
            اسألني عن الفروع، الحسابات، الخدمات الرقمية، أو البنوك الإسلامية.<br><br>
            Ask me about branches, accounts, digital banking, or Islamic services.
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg-block user-block">
                <div class="avatar-dot user-av">أ</div>
                <div class="bubble user-bubble">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-block">
                <div class="avatar-dot bot-av">BM</div>
                <div class="bubble bot-bubble">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ─── INPUT ─────────────────────────────────────────────────────────────────────

if prompt := st.chat_input("اكتب سؤالك هنا... / Type your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner(""):
        reply = ask_flowise(prompt, st.session_state.session_id)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
