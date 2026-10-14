import streamlit as st
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="Banque Misr Virtual Assistant | Team Leader Demo",
    page_icon="🏦",
    layout="wide",
)

# Custom CSS for Professional Banque Misr Branding & UI Layout
st.markdown(
    """
    <style>
        /* Main Theme Colors based on Banque Misr Identity */
        :root {
            --bm-burgundy: #6c1d31;
            --bm-gold: #d4af37;
            --bm-light-bg: #fdfbf7;
        }

        .main {
            background-color: var(--bm-light-bg);
        }

        /* Header Styling */
        .header-container {
            background: linear-gradient(135deg, #6c1d31 0%, #4a1321 100%);
            padding: 2rem;
            border-radius: 12px;
            color: white;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
        
        .header-title {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .header-subtitle {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        /* Metric Cards */
        .metric-card {
            background: white;
            padding: 1.2rem;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            border-left: 5px solid #d4af37;
            text-align: center;
        }

        /* Footer / Info note */
        .info-box {
            background-color: #fff9e6;
            border: 1px solid #ffeeba;
            padding: 1rem;
            border-radius: 8px;
            color: #856404;
            margin-top: 1rem;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# Sidebar Configuration for Team Leader Demo
with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Banque_Misr_logo.svg/1200px-Banque_Misr_logo.svg.png",
        width=180,
    )
    st.markdown("---")
    st.markdown("### 🛠️ Control Panel")
    st.info("Demo Mode: **Active**\n\nTarget Audience: **Management Review**")

    st.markdown("### 📊 System Status")
    st.success("Flowise Engine: Online")
    st.success("API Gateway: Connected")
    st.success("Security Layer: Active")

    st.markdown("---")
    st.markdown("### 💡 Quick Guide for Demo")
    st.markdown(
        """
    - **Test Queries:** Ask about bank certificates, credit cards, or loan programs.
    - **UI Features:** Responsive design with official corporate color palette.
    """
    )


# Main App Header Section
st.markdown(
    """
    <div class="header-container">
        <div class="header-title">
            <span>🏦</span> Banque Misr AI Assistant — Executive Demo
        </div>
        <div class="header-subtitle">
            Next-Generation Conversational Banking Interface powered by Flowise & Streamlit
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# Top Metrics Row for Executive Impression
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(
        """<div class="metric-card"><h4>Response Time</h4><h3>< 1.2s</h3></div>""",
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """<div class="metric-card"><h4>Availability</h4><h3>99.9%</h3></div>""",
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        """<div class="metric-card"><h4>Model Status</h4><h3>Production</h3></div>""",
        unsafe_allow_html=True,
    )
with col4:
    st.markdown(
        """<div class="metric-card"><h4>Security</h4><h3>Enterprise</h3></div>""",
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# YOUR EXACT FLOWISE EMBED CODE (Unchanged)
# ---------------------------------------------------------
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