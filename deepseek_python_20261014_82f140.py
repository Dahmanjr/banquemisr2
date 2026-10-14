# app.py
"""
Banque Misr Assistant — Streamlit frontend for a Flowise agent.
Run with:  streamlit run app.py

It talks to your Flowise chatflow:
    POST http://localhost:3000/api/v1/prediction/<FLOWISE_CHATFLOW_ID>
"""

import os
import requests
import streamlit as st

# ------------------------------------------------------------------------------
# Your agent configuration  (taken from the URL you gave me)
# ------------------------------------------------------------------------------
DEFAULT_FLOWISE_BASE = "http://localhost:3000"
DEFAULT_FLOWISE_ID   = "5570de1d-a438-4f08-928e-5732147b70f6"

# ------------------------------------------------------------------------------
# Page config
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Banque Misr Assistant",
    page_icon="🏦",
    layout="centered",
)

# ------------------------------------------------------------------------------
# Sidebar — agent config
# ------------------------------------------------------------------------------
with st.sidebar:
    st.title("🏦 Banque Misr")
    st.caption("Misr Assistant — powered by your Flowise agent")

    flowise_base = st.text_input(
        "Flowise base URL",
        value=os.getenv("FLOWISE_BASE", DEFAULT_FLOWISE_BASE),
    )
    flowise_id = st.text_input(
        "Chatflow ID",
        value=os.getenv("FLOWISE_ID", DEFAULT_FLOWISE_ID),
    )
    api_key = st.text_input(
        "Flowise API key (optional)",
        type="password",
        help="Only needed if your chatflow has an API key set in Flowise.",
    )

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()

    st.divider()
    st.caption("Official channels")
    st.markdown("- Call center: **19888**\n- Web: www.banquemisr.com")


# ------------------------------------------------------------------------------
# Agent call
# ------------------------------------------------------------------------------
def call_agent(question: str, history: list[dict]) -> str:
    """
    Send a message to the Flowise chatflow and return the reply text.

    Flowise history format:
        [{"role": "user", "content": "..."},
         {"role": "assistant", "content": "..."}]
    """
    url = f"{flowise_base.rstrip('/')}/api/v1/prediction/{flowise_id}"

    # Build history in Flowise's expected shape
    flowise_history = []
    for m in history:
        if m["role"] == "user":
            flowise_history.append({"role": "user", "content": m["content"]})
        elif m["role"] == "assistant":
            flowise_history.append({"role": "assistant", "content": m["content"]})

    payload = {
        "question": question,
        "history": flowise_history,
        # "overrideConfig": {...}   # uncomment if your flow needs it
    }
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=120)
        r.raise_for_status()
        data = r.json()

        # Flowise returns {"text": "...", ...} — some flows use "answer"
        return (
            data.get("text")
            or data.get("answer")
            or data.get("output")
            or "⚠️ Agent returned an empty response."
        )

    except requests.exceptions.ConnectionError:
        return (
            "⚠️ Could not reach the Flowise agent at "
            f"`{flowise_base}`.\n\n"
            "Make sure Flowise is running (`npx flowise start` or `npm start` "
            "in the Flowise folder) and the URL/ID are correct."
        )
    except requests.exceptions.HTTPError as e:
        return f"⚠️ Agent returned an HTTP error: `{e}`\n\nURL: `{url}`"
    except Exception as e:
        return f"⚠️ Unexpected error talking to the agent: `{e}`"


# ------------------------------------------------------------------------------
# Session state
# ------------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "أهلاً بيك في بنك مصر 🏦\n"
                "Welcome to Banque Misr! How can I help you today?\n\n"
                "I can help with accounts, cards, loans, transfers, "
                "branches and BM Online."
            ),
        }
    ]

# ------------------------------------------------------------------------------
# Header
# ------------------------------------------------------------------------------
st.title("🏦 Banque Misr Assistant")
st.caption(
    "Demo chatbot — not an official Banque Misr service. "
    "Never share your PIN, OTP or full card number."
)
st.caption(f"Connected agent: `{flowise_base}/chatbot/{flowise_id}`")

# ------------------------------------------------------------------------------
# Render history
# ------------------------------------------------------------------------------
for msg in st.session_state.messages:
    avatar = "🏦" if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ------------------------------------------------------------------------------
# Chat input
# ------------------------------------------------------------------------------
prompt = st.chat_input("اكتب سؤالك… / Type your question…")

if prompt:
    # show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # call agent
    with st.chat_message("assistant", avatar="🏦"):
        with st.spinner("Misr Assistant is typing…"):
            answer = call_agent(prompt, st.session_state.messages[:-1])
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})