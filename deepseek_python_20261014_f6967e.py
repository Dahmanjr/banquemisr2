# app.py
"""
Banque Misr Assistant — simple Streamlit chatbot
Run with:  streamlit run app.py
"""

import os
import streamlit as st

# ------------------------------------------------------------------------------
# Page config
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Banque Misr Assistant",
    page_icon="🏦",
    layout="centered",
)

# ------------------------------------------------------------------------------
# System prompt — the "brain" of the agent
# ------------------------------------------------------------------------------
SYSTEM_PROMPT = """
You are "Misr Assistant", the virtual assistant of Banque Misr (بنك مصر).

Rules:
- Be polite, concise and professional.
- Detect the user's language and answer in the SAME language (Egyptian Arabic / English).
- You help with: account opening, debit/credit cards, loans, transfers, IBAN,
  branches & ATMs, working hours, mobile banking (BM Online), fees and general FAQs.
- NEVER ask for or accept sensitive data: full card numbers, PINs, OTPs, passwords.
  If the user shares any, warn them to never share it and advise contacting the bank.
- You cannot perform real transactions. For anything account-specific, tell the user to:
    * call the call center: 19888 (inside Egypt)
    * visit the nearest branch
    * use BM Online / the mobile app
- If you don't know something or it may have changed (fees, rates, offers),
  say so clearly and refer the user to official Banque Misr channels
  (www.banquemisr.com, call center 19888).
- Keep answers short: 2-6 sentences or a short bullet list.
"""

# ------------------------------------------------------------------------------
# Tiny local knowledge base (used if no LLM API key is configured)
# ------------------------------------------------------------------------------
FAQ = [
    (("hour", "open", "close", "مواعيد", "تفتح", "تقفل"),
     "الفروع بتفتح عادة من الأحد للخميس، حوالي 8:30 صباحًا لحد 3:00 عصرًا "
     "(بعض الفروع ساعاتها مختلفة). Call center 19888 شغال 24/7."),
    (("call center", "hotline", "رقم", "خدمة العملاء"),
     "خدمة عملاء بنك مصر: 19888 من داخل مصر، أو +20 2 2391 5555 من الخارج."),
    (("atm", "ماكينة", "صراف"),
     "تقدر تلاقي أقرب ATM أو فرع من خلال موقع بنك مصر أو تطبيق BM Online "
     "عن طريق خدمة 'أقرب فرع / ماكينة'."),
    (("account", "open", "حساب", "أفتح"),
     "لفتح حساب: بطاقة الرقم القومي سارية + إثبات محل إقامة + الحد الأدنى للفتح. "
     "تقدر تبدأ من الفرع أو من تطبيق BM Online. الأرقام ممكن تتغير، فالأفضل تتأكد من 19888."),
    (("loan", "قرض", "تمويل"),
     "بنك مصر بيقدم قروض شخصية، قروض سيارات، وتمويل عقاري. الشروط والفوائد بتختلف "
     "حسب المبلغ ومدة السداد والدخل. اتصل بـ 19888 أو زور أقرب فرع لعرض مخصص."),
    (("card", "credit", "بطاقة", "فيزا", "ماستر"),
     "بنك مصر بيقدم بطاقات خصم وبطاقات ائتمانية (فيزا / ماستركارد) بفئات مختلفة. "
     "تقدر تطلبها من الفرع أو من BM Online لو عندك حساب قائم."),
    (("iban", "تحويل", "transfer", "سويفت", "swift"),
     "التحويلات المحلية بتحتاج رقم الحساب أو IBAN، والتحويلات الدولية بتحتاج "
     "SWIFT/BIC. تفاصيل عمولة التحويل بتتغير — اتأكد من 19888 أو من الفرع."),
    (("online", "app", "تطبيق", "اونلاين", "أونلاين"),
     "BM Online و تطبيق بنك مصر بيخلوك تتابع حسابك، تحوّل فلوس، تدفع فواتير، "
     "وتطلب خدمات من غير ما تروح الفرع. التسجيل بيتعمل من الفرع."),
]


def local_answer(text: str) -> str:
    """Very small keyword-based fallback so the app works without an API key."""
    low = text.lower()
    for keywords, answer in FAQ:
        if any(k in low for k in keywords):
            return answer
    return (
        "أنا مساعد بنك مصر 🏦\n\n"
        "أقدر أساعدك في: الحسابات، البطاقات، القروض، التحويلات، الفروع ومواعيد العمل، "
        "و BM Online.\n\n"
        "للتفاصيل الرسمية: **19888** أو **www.banquemisr.com**.\n\n"
        "⚠️ ملاحظة: الأسعار والعمولات بتتغير، فاتأكد دائمًا من المصادر الرسمية."
    )


# ------------------------------------------------------------------------------
# LLM client (optional)
# ------------------------------------------------------------------------------
def get_api_key() -> str:
    try:
        if "OPENAI_API_KEY" in st.secrets:
            return st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass
    return os.getenv("OPENAI_API_KEY", "")


@st.cache_resource(show_spinner=False)
def get_client(api_key: str, base_url: str):
    from openai import OpenAI
    return OpenAI(api_key=api_key, base_url=base_url or None)


# ------------------------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------------------------
with st.sidebar:
    st.title("🏦 Banque Misr")
    st.caption("Misr Assistant — virtual helper")

    api_key_input = st.text_input(
        "OpenAI API key (optional)",
        type="password",
        help="Leave empty to use the built-in offline FAQ mode.",
    )
    base_url = st.text_input(
        "Base URL (optional)",
        placeholder="https://api.openai.com/v1",
        help="Change this to use any OpenAI-compatible endpoint.",
    )
    model = st.text_input("Model", value="gpt-4o-mini")

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Official channels")
    st.markdown("- Call center: **19888**\n- Web: www.banquemisr.com")

api_key = api_key_input or get_api_key()
use_llm = bool(api_key)

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
                "I can help with accounts, cards, loans, transfers, branches and BM Online."
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
if not use_llm:
    st.info("Running in **offline FAQ mode**. Add an API key in the sidebar for full AI answers.")

# ------------------------------------------------------------------------------
# Render history
# ------------------------------------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🏦" if msg["role"] == "assistant" else None):
        st.markdown(msg["content"])

# ------------------------------------------------------------------------------
# Chat input
# ------------------------------------------------------------------------------
prompt = st.chat_input("اكتب سؤالك… / Type your question…")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🏦"):
        placeholder = st.empty()
        answer = ""

        if use_llm:
            try:
                client = get_client(api_key, base_url)
                stream = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}]
                    + [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    temperature=0.3,
                    max_tokens=600,
                    stream=True,
                )
                for chunk in stream:
                    delta = chunk.choices[0].delta.content or ""
                    answer += delta
                    placeholder.markdown(answer + "▌")
                placeholder.markdown(answer)

            except Exception as e:
                answer = f"⚠️ Connection error: `{e}`\n\n" + local_answer(prompt)
                placeholder.markdown(answer)
        else:
            answer = local_answer(prompt)
            placeholder.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})