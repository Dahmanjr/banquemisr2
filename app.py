import streamlit as st
import requests

# ── Config ────────────────────────────────────────────────────────────────────
API_URL = "http://localhost:3000/api/v1/prediction/5570de1d-a438-4f08-928e-5732147b70f6"

st.set_page_config(
    page_title="Banque Misr Assistant",
    page_icon="🏦",
    layout="centered",
)

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Global ── */
    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }

    /* ── Header ── */
    .bm-header {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 18px 24px;
        background: linear-gradient(135deg, #00703C 0%, #005a30 100%);
        border-radius: 12px;
        margin-bottom: 24px;
    }
    .bm-header-text h1 {
        color: #ffffff;
        font-size: 1.45rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
    }
    .bm-header-text p {
        color: #a8d5b5;
        font-size: 0.82rem;
        margin: 2px 0 0;
    }

    /* ── Chat bubbles ── */
    .msg-row { display: flex; margin-bottom: 14px; align-items: flex-end; gap: 10px; }
    .msg-row.user  { flex-direction: row-reverse; }
    .msg-row.bot   { flex-direction: row; }

    .avatar {
        width: 36px; height: 36px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.1rem; flex-shrink: 0;
    }
    .avatar.bot  { background: #00703C; color: #fff; }
    .avatar.user { background: #e8f5e9; color: #00703C; }

    .bubble {
        max-width: 75%;
        padding: 11px 16px;
        border-radius: 16px;
        font-size: 0.93rem;
        line-height: 1.55;
        word-wrap: break-word;
    }
    .bubble.bot  {
        background: #f0f9f4;
        border: 1px solid #c8e6c9;
        color: #1a1a1a;
        border-bottom-left-radius: 4px;
    }
    .bubble.user {
        background: #00703C;
        color: #ffffff;
        border-bottom-right-radius: 4px;
    }

    /* ── Typing indicator ── */
    .typing { display: flex; gap: 5px; padding: 8px 14px; }
    .typing span {
        width: 8px; height: 8px; border-radius: 50%;
        background: #00703C; opacity: 0.4;
        animation: blink 1.2s infinite;
    }
    .typing span:nth-child(2) { animation-delay: 0.2s; }
    .typing span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes blink { 0%,80%,100%{opacity:.4} 40%{opacity:1} }

    /* ── Input area ── */
    .stTextInput > div > div > input {
        border: 1.5px solid #c8e6c9 !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        font-size: 0.93rem !important;
        transition: border-color .2s;
    }
    .stTextInput > div > div > input:focus {
        border-color: #00703C !important;
        box-shadow: 0 0 0 3px rgba(0,112,60,.12) !important;
    }
    .stButton > button {
        background: #00703C !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 22px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: background .2s;
    }
    .stButton > button:hover { background: #005a30 !important; }

    /* ── Footer ── */
    .bm-footer {
        text-align: center;
        font-size: 0.75rem;
        color: #9e9e9e;
        margin-top: 18px;
        padding-top: 12px;
        border-top: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="bm-header">
    <div style="font-size:2.2rem">🏦</div>
    <div class="bm-header-text">
        <h1>Banque Misr Assistant</h1>
        <p>مرحباً بك · أنا هنا لمساعدتك في كل استفساراتك البنكية</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "bot",
            "content": (
                "أهلاً وسهلاً! أنا المساعد الذكي لبنك مصر. 🌿\n\n"
                "يمكنني مساعدتك في:\n"
                "• الاستفسار عن الحسابات والبطاقات\n"
                "• خدمات القروض والتمويل\n"
                "• الحوالات والمدفوعات\n"
                "• فروع وماكينات ATM\n\n"
                "كيف أستطيع مساعدتك اليوم؟"
            ),
        }
    ]

# ── API call ──────────────────────────────────────────────────────────────────
def ask_flowise(question: str) -> str:
    try:
        resp = requests.post(API_URL, json={"question": question}, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        # FlowiseAI returns {"text": "..."} or {"answer": "..."}
        return data.get("text") or data.get("answer") or str(data)
    except requests.exceptions.ConnectionError:
        return "⚠️ لا يمكن الاتصال بالخادم حالياً. يرجى التحقق من تشغيل Flowise."
    except requests.exceptions.Timeout:
        return "⚠️ انتهت مهلة الاتصال. يرجى المحاولة مرة أخرى."
    except Exception as e:
        return f"⚠️ حدث خطأ: {str(e)}"

# ── Chat history ──────────────────────────────────────────────────────────────
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        role = msg["role"]
        icon = "🏦" if role == "bot" else "👤"
        st.markdown(f"""
        <div class="msg-row {role}">
            <div class="avatar {role}">{icon}</div>
            <div class="bubble {role}">{msg["content"].replace(chr(10), "<br>")}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input(
        "message",
        placeholder="اكتب رسالتك هنا... / Type your message here...",
        label_visibility="collapsed",
        key="input_field",
    )
with col2:
    send = st.button("إرسال", use_container_width=True)

# ── Handle send ───────────────────────────────────────────────────────────────
if send and user_input.strip():
    question = user_input.strip()
    st.session_state.messages.append({"role": "user", "content": question})

    with st.spinner("جاري المعالجة..."):
        answer = ask_flowise(question)

    st.session_state.messages.append({"role": "bot", "content": answer})
    st.rerun()

# ── Quick suggestions ─────────────────────────────────────────────────────────
if len(st.session_state.messages) <= 1:
    st.markdown("<br>**اقتراحات سريعة:**", unsafe_allow_html=True)
    suggestions = [
        "ما هي أنواع الحسابات المتاحة؟",
        "كيف أفتح حساب جديد؟",
        "ما هي شروط القرض الشخصي؟",
        "أين أقرب فرع مني؟",
    ]
    cols = st.columns(2)
    for i, suggestion in enumerate(suggestions):
        if cols[i % 2].button(suggestion, key=f"sug_{i}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": suggestion})
            with st.spinner("جاري المعالجة..."):
                answer = ask_flowise(suggestion)
            st.session_state.messages.append({"role": "bot", "content": answer})
            st.rerun()

# ── Clear chat ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/3/30/Banque_Misr_logo.svg/200px-Banque_Misr_logo.svg.png", width=160)
    st.markdown("---")
    st.markdown("### إعدادات المحادثة")
    if st.button("🗑️ مسح المحادثة", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "bot",
                "content": "أهلاً من جديد! كيف أستطيع مساعدتك؟ 🌿",
            }
        ]
        st.rerun()
    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.8rem; color:#666;">
    <b>خط خدمة العملاء</b><br>
    📞 19888<br><br>
    <b>متاح على مدار الساعة</b><br>
    للاستفسارات الطارئة
    </div>
    """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="bm-footer">
    بنك مصر © 2024 · هذا المساعد للمعلومات العامة فقط · للمعاملات الرسمية تواصل مع أقرب فرع
</div>
""", unsafe_allow_html=True)
