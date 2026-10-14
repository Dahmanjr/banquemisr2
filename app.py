import streamlit as st
import requests
import base64
from pathlib import Path

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Banque Misr Assistant",
    page_icon="🏦",
    layout="centered",
)

# ── API ───────────────────────────────────────────────────────────────────────
API_URL = "http://localhost:3000/api/v1/prediction/5570de1d-a438-4f08-928e-5732147b70f6"

def query(question: str) -> str:
    try:
        response = requests.post(API_URL, json={"question": question}, timeout=60)
        response.raise_for_status()
        data = response.json()
        # FlowiseAI returns {"text": "..."} or {"answer": "..."}
        return data.get("text") or data.get("answer") or str(data)
    except requests.exceptions.ConnectionError:
        return "⚠️ Could not connect to the assistant service. Please make sure the server is running."
    except Exception as e:
        return f"⚠️ An error occurred: {str(e)}"

# ── Logo (embed from uploaded file) ──────────────────────────────────────────
LOGO_PATH = "/mnt/user-data/uploads/1791984365055_image.png"

def get_logo_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_b64 = get_logo_base64(LOGO_PATH)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  /* Import typefaces */
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=Inter:wght@400;500&display=swap');

  /* Reset & base */
  html, body, [data-testid="stAppViewContainer"] {{
    background: #7A1832 !important;
    font-family: 'Inter', sans-serif;
  }}

  /* Hide Streamlit chrome */
  #MainMenu, footer, header {{ visibility: hidden; }}
  [data-testid="stToolbar"] {{ display: none; }}

  /* Main content wrapper */
  [data-testid="stAppViewContainer"] > .main > .block-container {{
    max-width: 780px;
    padding: 2rem 1.5rem 6rem;
    margin: 0 auto;
  }}

  /* ── Header ── */
  .bm-header {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
    padding: 2rem 0 1.5rem;
  }}
  .bm-header img {{
    width: 130px;
    height: 130px;
    object-fit: contain;
    filter: drop-shadow(0 4px 16px rgba(0,0,0,.4));
  }}
  .bm-title {{
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.65rem;
    font-weight: 700;
    color: #F0C040;
    letter-spacing: .02em;
    margin: 0;
    text-align: center;
  }}
  .bm-subtitle {{
    font-size: 0.85rem;
    color: rgba(255,255,255,.65);
    margin: 0;
    text-align: center;
    letter-spacing: .03em;
  }}
  .bm-divider {{
    width: 60px;
    height: 2px;
    background: #C4973A;
    border: none;
    margin: 0.5rem auto 0;
    border-radius: 2px;
  }}

  /* ── Chat bubbles ── */
  .chat-area {{
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }}
  .bubble-row {{
    display: flex;
    align-items: flex-end;
    gap: 0.6rem;
  }}
  .bubble-row.user {{ justify-content: flex-end; }}
  .bubble-row.assistant {{ justify-content: flex-start; }}

  .avatar {{
    width: 34px;
    height: 34px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
  }}
  .avatar.bot {{
    background: #C4973A;
    color: #5A1020;
    font-weight: 700;
  }}
  .avatar.usr {{
    background: rgba(255,255,255,.15);
    color: #fff;
  }}

  .bubble {{
    max-width: 72%;
    padding: 0.75rem 1.1rem;
    border-radius: 18px;
    font-size: 0.92rem;
    line-height: 1.55;
  }}
  .bubble.user {{
    background: #C4973A;
    color: #3B0A18;
    border-bottom-right-radius: 4px;
    font-weight: 500;
  }}
  .bubble.assistant {{
    background: rgba(255,255,255,.1);
    color: #F5F0E8;
    border: 1px solid rgba(196,151,58,.25);
    border-bottom-left-radius: 4px;
  }}

  /* Typing indicator */
  .typing-indicator {{
    display: flex;
    gap: 5px;
    padding: 0.6rem 1rem;
    align-items: center;
  }}
  .dot {{
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #C4973A;
    animation: bounce 1.2s infinite;
  }}
  .dot:nth-child(2) {{ animation-delay: .2s; }}
  .dot:nth-child(3) {{ animation-delay: .4s; }}
  @keyframes bounce {{
    0%, 60%, 100% {{ transform: translateY(0); opacity: .6; }}
    30% {{ transform: translateY(-6px); opacity: 1; }}
  }}

  /* ── Input bar ── */
  /* Stick to bottom */
  .stBottom > div {{
    background: transparent !important;
    padding: 1rem 0 0.5rem;
  }}
  [data-testid="stChatInput"] {{
    background: rgba(255,255,255,.1) !important;
    border: 1px solid rgba(196,151,58,.4) !important;
    border-radius: 14px !important;
    color: #fff !important;
  }}
  [data-testid="stChatInput"] textarea {{
    color: #fff !important;
    background: transparent !important;
    font-family: 'Inter', sans-serif;
    font-size: 0.92rem;
  }}
  [data-testid="stChatInput"] textarea::placeholder {{
    color: rgba(255,255,255,.4) !important;
  }}
  [data-testid="stChatInputSubmitButton"] svg {{
    fill: #C4973A !important;
  }}

  /* ── Welcome card ── */
  .welcome-card {{
    background: rgba(255,255,255,.07);
    border: 1px solid rgba(196,151,58,.3);
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1.5rem;
    color: rgba(255,255,255,.8);
    font-size: 0.88rem;
    line-height: 1.6;
    text-align: center;
  }}
  .welcome-card strong {{
    color: #F0C040;
  }}

  /* Quick chips */
  .chips {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    justify-content: center;
    margin-top: 1rem;
  }}
  .chip {{
    background: rgba(196,151,58,.18);
    border: 1px solid rgba(196,151,58,.45);
    color: #F0C040;
    border-radius: 20px;
    padding: 0.35rem 0.9rem;
    font-size: 0.8rem;
    cursor: pointer;
    transition: background .2s;
  }}
  .chip:hover {{ background: rgba(196,151,58,.35); }}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="bm-header">
  <img src="data:image/png;base64,{logo_b64}" alt="Banque Misr Logo"/>
  <p class="bm-title">Banque Misr Assistant</p>
  <p class="bm-subtitle">مساعدك الذكي · Your Smart Banking Assistant</p>
  <hr class="bm-divider"/>
</div>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Welcome card (shown only before first message) ────────────────────────────
QUICK_PROMPTS = [
    "What accounts do you offer?",
    "كيف أفتح حساب؟",
    "What are your interest rates?",
    "Nearest branch to me",
]

if not st.session_state.messages:
    chips_html = "".join(
        f'<span class="chip" onclick="void(0)">{p}</span>' for p in QUICK_PROMPTS
    )
    st.markdown(f"""
    <div class="welcome-card">
      <strong>Welcome to Banque Misr! 🏛️</strong><br/>
      أهلاً بك في بنك مصر — How can we help you today?<br/>
      Ask anything about our products, branches, or services.
      <div class="chips">{chips_html}</div>
    </div>
    """, unsafe_allow_html=True)

    # Streamlit buttons for quick prompts (functional)
    cols = st.columns(len(QUICK_PROMPTS))
    for col, prompt in zip(cols, QUICK_PROMPTS):
        if col.button(prompt, key=f"chip_{prompt}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.spinner(""):
                reply = query(prompt)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()

# ── Render chat history ───────────────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="bubble-row user">
          <div class="bubble user">{msg['content']}</div>
          <div class="avatar usr">👤</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="bubble-row assistant">
          <div class="avatar bot">B</div>
          <div class="bubble assistant">{msg['content']}</div>
        </div>""", unsafe_allow_html=True)

# ── Chat input ────────────────────────────────────────────────────────────────
if user_input := st.chat_input("Ask me anything about Banque Misr…"):
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Render user bubble immediately
    st.markdown(f"""
    <div class="bubble-row user">
      <div class="bubble user">{user_input}</div>
      <div class="avatar usr">👤</div>
    </div>""", unsafe_allow_html=True)

    # Typing indicator
    typing_placeholder = st.empty()
    typing_placeholder.markdown("""
    <div class="bubble-row assistant">
      <div class="avatar bot">B</div>
      <div class="bubble assistant">
        <div class="typing-indicator">
          <div class="dot"></div><div class="dot"></div><div class="dot"></div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    reply = query(user_input)
    typing_placeholder.empty()

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
