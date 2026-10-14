import streamlit as st
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="Banque Misr Virtual Assistant",
    page_icon="🏦",
    layout="wide",
)

# App Header
st.title("🏦 Banque Misr Assistant Chatbot")
st.markdown(
    "Welcome! Feel free to interact with the Banque Misr virtual assistant"
    " widget below."
)

# Flowise Embed Chatbot HTML/JS Code
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
# height is set to 700 pixels so the floating chat bubble has room to expand
components.html(flowise_embed_code, height=700)