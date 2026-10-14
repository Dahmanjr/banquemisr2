"""Banque Misr virtual assistant: Streamlit front end for a Flowise agent."""

import base64
import os
import uuid
from pathlib import Path

import requests
import streamlit as st

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------
# Locally this points at your Flowise server. When you deploy to Streamlit
# Cloud, set FLOWISE_API_URL in the app's Secrets to a publicly reachable URL.
DEFAULT_API_URL = (
    "http://localhost:3000/api/v1/prediction/5570de1d-a438-4f08-928e-5732147b70f6"
)


def get_setting(name: str, default: str = "") -> str:
    try:
        if name in st.secrets:
            return str(st.secrets[name])
    except Exception:  # no secrets.toml present
        pass
    return os.getenv(name, default)


API_URL = get_setting("FLOWISE_API_URL", DEFAULT_API_URL)
API_KEY = get_setting("FLOWISE_API_KEY")  # optional
LOGO_PATH = Path(__file__).parent / "banque_misr_logo.png"

MAROON = "#862F40"
GOLD = "#E3A91B"

st.set_page_config(
    page_title="Banque Misr Assistant",
    page_icon=str(LOGO_PATH) if LOGO_PATH.exists() else "🏦",
    layout="centered",
)

# --------------------------------------------------------------------------
# Styling
# --------------------------------------------------------------------------
def logo_b64() -> str:
    return base64.b64encode(LOGO_PATH.read_bytes()).decode() if LOGO_PATH.exists() else ""


CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stApp, button, input, textarea {{
    font-family: 'Cairo', sans-serif !important;
}}
#MainMenu, footer, [data-testid="stDecoration"] {{ visibility: hidden; }}
.block-container {{ padding-top: 1.2rem; max-width: 780px; }}

/* ---------- header ---------- */
.bm-header {{
    display: flex; align-items: center; gap: 16px;
    background: {MAROON}; color: #fff;
    padding: 16px 20px; border-radius: 14px;
    border-bottom: 4px solid {GOLD};
    margin-bottom: 1.2rem;
}}
.bm-header img {{ width: 60px; height: 60px; border-radius: 10px; }}
.bm-header h1 {{
    font-size: 1.45rem; font-weight: 700; margin: 0; padding: 0;
    color: #fff; line-height: 1.25;
}}
.bm-header p {{ margin: 2px 0 0; font-size: .92rem; color: #F2DDE1; }}

/* ---------- messages ---------- */
[data-testid="stChatMessage"] {{
    border-radius: 14px; padding: 12px 16px; margin-bottom: 10px;
    background: #fff; border: 1px solid #E8DDD2;
    border-left: 4px solid {MAROON};
}}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
    background: #FBF1D9; border: 1px solid #F0DDAA;
    border-left: 4px solid {GOLD};
}}
/* Arabic and English both render in the right direction */
[data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li {{
    unicode-bidi: plaintext; text-align: start; line-height: 1.7;
}}

/* ---------- input ---------- */
[data-testid="stChatInput"] {{ border-radius: 14px; border-color: {MAROON}; }}
[data-testid="stChatInput"]:focus-within {{
    border-color: {MAROON}; box-shadow: 0 0 0 2px {MAROON}33;
}}
[data-testid="stChatInput"] button {{ background: {MAROON}; color: #fff; }}

/* ---------- suggestion buttons (main area) ---------- */
.stMain .stButton > button {{
    width: 100%; text-align: start; justify-content: flex-start;
    background: #fff; color: {MAROON}; border: 1px solid #DCC9BC;
    border-radius: 12px; padding: .65rem .9rem; font-weight: 500;
    transition: border-color .15s, background .15s;
}}
.stMain .stButton > button:hover {{
    border-color: {GOLD}; background: #FFF8E6; color: {MAROON};
}}
.bm-hint {{ color: #6B5A5D; font-size: .95rem; margin: .2rem 0 .8rem; }}

/* ---------- sidebar ---------- */
[data-testid="stSidebar"] {{ background: {MAROON}; }}
[data-testid="stSidebar"] * {{ color: #fff; }}
[data-testid="stSidebar"] a {{ color: {GOLD}; text-decoration: none; }}
[data-testid="stSidebar"] hr {{ border-color: #ffffff33; }}
[data-testid="stSidebar"] .stButton > button {{
    background: transparent; border: 1px solid {GOLD}; color: {GOLD};
    border-radius: 10px; width: 100%;
}}
[data-testid="stSidebar"] .stButton > button:hover {{
    background: {GOLD}; color: {MAROON};
}}
.bm-side-block {{ font-size: .92rem; line-height: 1.7; }}
.bm-side-block b {{ color: {GOLD}; font-weight: 600; }}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# --------------------------------------------------------------------------
# State
# --------------------------------------------------------------------------
WELCOME = (
    "Welcome to Banque Misr. I can help with branches, accounts, Islamic banking, "
    "BM Online and BM Wallet. You can write in English or Arabic.\n\n"
    "أهلاً بك في بنك مصر. اسألني عن الفروع والخدمات المصرفية."
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())  # keeps Flowise memory per visitor
if "queued" not in st.session_state:
    st.session_state.queued = None

SUGGESTIONS = [
    "When was Banque Misr founded?",
    "How do I find the nearest branch or ATM?",
    "What is BM Wallet?",
    "Does Banque Misr offer Islamic banking?",
    "What is the customer service hotline?",
    "ما هي خدمات بنك مصر الرقمية؟",
]

def candidate_urls() -> list[str]:
    """Try the configured URL first; if it uses localhost, also try 127.0.0.1
    (some machines resolve localhost to IPv6 while Flowise listens on IPv4)."""
    urls = [API_URL]
    if "://localhost" in API_URL:
        urls.append(API_URL.replace("://localhost", "://127.0.0.1"))
    return urls


def host_of(url: str) -> str:
    return "/".join(url.split("/")[:3])  # scheme://host:port only


def check_connection() -> tuple[bool, str]:
    """Ping the Flowise server (not the agent) to see if it is reachable."""
    for url in candidate_urls():
        base = host_of(url)
        try:
            r = requests.get(f"{base}/api/v1/ping", timeout=5)
            return True, f"Connected to {base} (HTTP {r.status_code})."
        except requests.exceptions.RequestException:
            continue
    return False, f"Cannot reach {host_of(API_URL)}. Is Flowise running?"


# --------------------------------------------------------------------------
# Flowise call
# --------------------------------------------------------------------------
def ask_agent(question: str) -> str:
    headers = {"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}
    payload = {
        "question": question,
        "overrideConfig": {"sessionId": st.session_state.session_id},
    }
    last_error = ""
    for url in candidate_urls():
        try:
            r = requests.post(url, json=payload, headers=headers, timeout=90)
            r.raise_for_status()
            data = r.json()
            return data.get("text") or data.get("answer") or "Sorry, I received an empty reply."
        except requests.exceptions.ConnectionError as e:
            last_error = f"Could not connect to `{host_of(url)}` ({type(e).__name__})."
        except requests.exceptions.Timeout:
            return "The assistant took too long to answer. Please try again."
        except requests.exceptions.HTTPError as e:
            code = e.response.status_code
            hint = " Set `FLOWISE_API_KEY`." if code in (401, 403) else ""
            return f"The assistant service returned error {code}.{hint}"
        except ValueError:
            return "The assistant service sent a reply I couldn't read."
    return (
        f"{last_error} Make sure Flowise is running, and if this app is deployed online, "
        "set `FLOWISE_API_URL` to a public Flowise address (localhost only works on your own computer)."
    )


# --------------------------------------------------------------------------
# Sidebar
# --------------------------------------------------------------------------
with st.sidebar:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), use_container_width=True)
    st.markdown(
        """
<div class="bm-side-block">
<b>Customer service</b><br>19888 (Egypt hotline)<br><br>
<b>Website</b><br><a href="https://www.banquemisr.com" target="_blank">www.banquemisr.com</a><br><br>
<b>Mobile app</b><br>BM Online for iOS and Android
</div>
""",
        unsafe_allow_html=True,
    )
    st.divider()
    if st.button("Start a new chat"):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()
    if st.button("Test connection"):
        ok, msg = check_connection()
        (st.success if ok else st.error)(msg)
    st.divider()
    st.caption("Demo assistant. For account-specific help, call 19888 or visit a branch. "
               "Never share your PIN, password or OTP in this chat.")

# --------------------------------------------------------------------------
# Header
# --------------------------------------------------------------------------
st.markdown(
    f"""
<div class="bm-header">
  <img src="data:image/png;base64,{logo_b64()}" alt="Banque Misr logo">
  <div>
    <h1>Banque Misr Assistant</h1>
    <p>Ask about branches, accounts, digital banking and more.</p>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

AVATAR_BOT = str(LOGO_PATH) if LOGO_PATH.exists() else "🏦"

# --------------------------------------------------------------------------
# Conversation
# --------------------------------------------------------------------------
with st.chat_message("assistant", avatar=AVATAR_BOT):
    st.markdown(WELCOME)

for m in st.session_state.messages:
    with st.chat_message(m["role"], avatar=AVATAR_BOT if m["role"] == "assistant" else None):
        st.markdown(m["content"])

# Suggestions only before the first question
if not st.session_state.messages:
    st.markdown('<p class="bm-hint">Try one of these:</p>', unsafe_allow_html=True)
    cols = st.columns(2)
    for i, text in enumerate(SUGGESTIONS):
        if cols[i % 2].button(text, key=f"sug_{i}"):
            st.session_state.queued = text
            st.rerun()

# --------------------------------------------------------------------------
# Input
# --------------------------------------------------------------------------
typed = st.chat_input("Type your question here… / اكتب سؤالك هنا")
prompt = typed or st.session_state.queued
st.session_state.queued = None

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=AVATAR_BOT):
        with st.spinner("Looking that up…"):
            answer = ask_agent(prompt)
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    if len(st.session_state.messages) == 2:
        st.rerun()  # first exchange: refresh so the suggestion buttons disappear
