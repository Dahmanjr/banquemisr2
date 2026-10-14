"""Banque Misr Virtual Assistant – Streamlit app."""

import os
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Banque Misr Virtual Assistant",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DEFAULT_API_HOST = "http://localhost:3000"
DEFAULT_CHATFLOW_ID = "5570de1d-a438-4f08-928e-5732147b70f6"


def get_setting(name: str, default: str) -> str:
    """Read from Streamlit secrets, then environment variables, then default."""
    try:
        if name in st.secrets:
            return str(st.secrets[name])
    except Exception:
        pass
    return os.environ.get(name, default)


API_HOST = get_setting("FLOWISE_API_HOST", DEFAULT_API_HOST).rstrip("/")
CHATFLOW_ID = get_setting("FLOWISE_CHATFLOW_ID", DEFAULT_CHATFLOW_ID)

# Remove Streamlit's own chrome/padding so the page fills the frame
st.markdown(
    """
    <style>
      #MainMenu, header, footer {visibility: hidden;}
      .block-container {padding: 0 !important; max-width: 100% !important;}
      iframe {border: none; width: 100%;}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_html(api_host: str, chatflow_id: str) -> str:
    html = (Path(__file__).parent / "assistant_ui.html").read_text(encoding="utf-8")
    html = html.replace(f'apiHost: "{DEFAULT_API_HOST}"', f'apiHost: "{api_host}"')
    html = html.replace(f'chatflowid: "{DEFAULT_CHATFLOW_ID}"', f'chatflowid: "{chatflow_id}"')
    return html


if "localhost" in API_HOST or "127.0.0.1" in API_HOST:
    st.warning(
        "Flowise is set to a localhost address. This only works on your own machine. "
        "Set `FLOWISE_API_HOST` to your public Flowise URL when deploying.",
        icon="⚠️",
    )

page_html = load_html(API_HOST, CHATFLOW_ID)

# st.iframe is the current API; st.components.v1.html is deprecated.
if hasattr(st, "iframe"):
    st.iframe(page_html, height=950)
else:  # older Streamlit versions
    components.html(page_html, height=950, scrolling=True)
