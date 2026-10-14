import streamlit as st
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="Banque Misr Virtual Assistant",
    page_icon="🏦",
    layout="wide",
)

# Custom CSS for enhanced UI and Banque Misr branding
st.markdown(
    """
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stApp header {
        background-color: transparent;
    }
    .welcome-card {
        background: linear-gradient(135deg, #7A1320 0%, #4A0B12 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .welcome-card h1 {
        color: #ffffff;
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
    }
    .welcome-card p {
        color: #f0f0f0;
        font-size: 1.1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar with Logo and Navigation/Info
with st.sidebar:
    st.image("banque_misr_logo.jpg", use_container_width=True)
    st.markdown("---")
    st.markdown("### 🌟 About the Assistant")
    st.markdown(
        "Your 24/7 digital banking companion. Ask about accounts, loans,"
        " certificates, and services."
    )
    st.markdown("---")
    st.markdown("### 📞 Quick Support")
    st.markdown(
        "- **Hotline:** 19888\n- **International:** +202 19888\n- **Email:**"
        " info@banquemisr.com"
    )

# Main App Header with Custom Styled Banner
st.markdown(
    """
    <div class="welcome-card">
        <h1>🏦 Banque Misr Virtual Assistant</h1>
        <p>Welcome! Experience seamless digital banking support. Feel free to interact with the virtual assistant widget below.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Flowise Embed Chatbot HTML/JS Code (Unchanged)
flowise_embed_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Banque Misr Assistant</title>
</head>
<body>
    <script type="module">
        import Chatbot from "https://cdn.jsdelivr.net/npm/flowise-embed/dist/web.js"
        Chatbot.init({
            chatflowid: "5570de1d-a438-4f08-928e-5732147b70f6",
            apiHost: "http://localhost:3000",
            theme: {
                button: {
                    backgroundColor: "#b30000", /* Banque Misr brand red-ish tone or customize */
                    right: 20,
                    bottom: 20,
                    size: 48,
                    iconColor: "white",
                },
                chatWindow: {
                    showTitle: true,
                    title: 'Banque Misr Assistant',
                    welcomeMessage: 'Hello! How can I help you with Banque Misr today?',
                    backgroundColor: "#ffffff",
                    height: 600,
                    width: 400,
                }
            }
        })
    </script>
</body>
</html>
"""

# Render the widget inside Streamlit using components.html
components.html(flowise_embed_code, height=700)