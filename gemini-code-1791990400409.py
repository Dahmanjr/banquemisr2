import base64
import os
import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(
    page_title="Banque Misr AI Assistant",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Helper function to encode image to Base64 for CSS/HTML rendering
def get_image_base64(image_path):
  if os.path.exists(image_path):
    with open(image_path, "rb") as img_file:
      return base64.b64encode(img_file.read()).decode()
  return ""


logo_b64 = get_image_base64("banque_misr_logo.jpg")

# 2. Custom CSS for Banque Misr Branding (Burgundy & Gold Theme)
custom_css = f"""
<style>
    /* Main App Background & Font Styling */
    .stApp {{
        background-color: #fdfbf7;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    
    /* Header Container */
    .header-container {{
        background: linear-gradient(135deg, #7A1228 0%, #520B1A 100%);
        padding: 30px;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        margin-bottom: 25px;
        border-bottom: 4px solid #C5A059;
    }}
    
    .header-logo {{
        max-width: 140px;
        margin-bottom: 15px;
        border-radius: 8px;
    }}
    
    .header-title {{
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: 0.5px;
    }}
    
    .header-subtitle {{
        color: #E2C98A;
        font-size: 1.1rem;
        margin-top: 8px;
        font-weight: 400;
    }}

    /* Card Containers */
    .feature-card {{
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #e2d8c3;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        margin-bottom: 15px;
    }}
    
    .feature-card h4 {{
        color: #7A1228;
        margin-top: 0;
        margin-bottom: 8px;
    }}
    
    .feature-card p {{
        color: #555555;
        font-size: 0.92rem;
        margin: 0;
    }}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }}
    
    /* Custom Badge */
    .status-badge {{
        background-color: #e6f4ea;
        color: #137333;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-top: 10px;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 3. Sidebar Setup
with st.sidebar:
  if logo_b64:
    st.image("banque_misr_logo.jpg", use_container_width=True)
  else:
    st.title("🏛️ Banque Misr")

  st.markdown("---")
  st.markdown("### 💡 Quick Assistance")
  st.info("Ask your questions in the chat bubble on the right about:")
  st.markdown("""
    - 💳 **Accounts & Cards**
    - 📈 **Certificates of Deposit**
    - 🏦 **Loan Programs**
    - 📍 **Branch & ATM Locations**
    - 🌐 **BM Online Services**
    """)

  st.markdown("---")
  st.markdown("<div class='status-badge'>🟢 AI Agent Active</div>", unsafe_allow_html=True)
  st.caption("Powered by Flowise AI Backend")


# 4. Header Section
header_html = f"""
<div class="header-container">
    {'<img src="data:image/jpeg;base64,' + logo_b64 + '" class="header-logo" alt="Banque Misr Logo">' if logo_b64 else ''}
    <h1 class="header-title">Banque Misr Virtual Assistant</h1>
    <div class="header-subtitle">مساعد بنك مصر الذكي - Your 24/7 Smart Financial Companion</div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# 5. Features / Quick Info Grid
col1, col2, col3 = st.columns(3)

with col1:
  st.markdown(
      """
    <div class="feature-card">
        <h4>🏦 Accounts & Saving</h4>
        <p>Explore high-yield savings accounts and certificate options suited for your needs.</p>
    </div>
    """,
      unsafe_allow_html=True,
  )

with col2:
  st.markdown(
      """
    <div class="feature-card">
        <h4>💳 Cards & Loans</h4>
        <p>Inquire about credit cards, personal loans, car loans, and mortgage options.</p>
    </div>
    """,
      unsafe_allow_html=True,
  )

with col3:
  st.markdown(
      """
    <div class="feature-card">
        <h4>🌐 BM Online</h4>
        <p>Get instant guidance on internet banking, mobile apps, and digital transfers.</p>
    </div>
    """,
      unsafe_allow_html=True,
  )

# 6. Flowise Embedded Chatbot Widget HTML/JS
flowise_embed_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
    </style>
</head>
<body>
    <script type="module">
        import Chatbot from "https://cdn.jsdelivr.net/npm/flowise-embed/dist/web.js"
        Chatbot.init({
            chatflowid: "5570de1d-a438-4f08-928e-5732147b70f6",
            apiHost: "http://localhost:3000",
            theme: {
                button: {
                    backgroundColor: "#7A1228", /* Banque Misr Burgundy */
                    right: 30,
                    bottom: 30,
                    size: 56,
                    dragAndDrop: false,
                    iconColor: "#C5A059", /* Banque Misr Gold */
                    customIconSrc: "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/bank.png",
                },
                chatWindow: {
                    showTitle: true,
                    title: 'Banque Misr Assistant',
                    welcomeMessage: 'مرحباً بك في بنك مصر! كيف يمكنني مساعدتك اليوم؟\n\nWelcome to Banque Misr! How can I help you today?',
                    backgroundColor: "#ffffff",
                    height: 580,
                    width: 400,
                    fontSize: 15,
                    poweredByTextColor: "#7A1228",
                    botMessage: {
                        backgroundColor: "#f0f2f5",
                        textColor: "#1c1e21",
                        showAvatar: true,
                        avatarSrc: "https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/png/bank.png",
                    },
                    userMessage: {
                        backgroundColor: "#7A1228",
                        textColor: "#ffffff",
                        showAvatar: false,
                    },
                    textInput: {
                        placeholder: 'Type your question here...',
                        backgroundColor: "#ffffff",
                        textColor: "#333333",
                        sendButtonColor: "#7A1228",
                    }
                }
            }
        })
    </script>
</body>
</html>
"""

# Render the widget inside Streamlit
components.html(flowise_embed_code, height=650)