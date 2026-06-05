
import streamlit as st
import requests

# ==================================================
# CONFIG
# ==================================================

API_URL = "https://web-production-487a0.up.railway.app/chat"

st.set_page_config(
    page_title="Riya Shah AI",
    page_icon="🤖",
    layout="centered"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.block-container{
    max-width:850px;
    padding-top:2rem;
}

.main{
    background-color:#fafafa;
}

.hero{
    text-align:center;
    padding-bottom:20px;
}

.hero-title{
    font-size:3.2rem;
    font-weight:700;
    margin-bottom:0px;
}

.hero-sub{
    font-size:1.1rem;
    color:#808080;
    max-width:700px;
    margin:auto;
}

.footer{
    text-align:center;
    color:#9a9a9a;
    font-size:13px;
    margin-top:40px;
}

div[data-testid="stChatMessage"]{
    border-radius:18px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("🤖 Riya Shah AI")

    st.markdown("---")

    st.write("""
Hi! I'm an AI version of **Riya Shah**.

I've been built using her:

- 🎓 Resume
- 🚀 Projects
- 📂 GitHub Repositories
- 💼 Internship Experience
- 🤖 AI / ML Work

Instead of searching through documents,
you can simply chat with me.
""")

    st.markdown("---")

    st.subheader("🧠 I can help with")

    st.markdown("""
✅ Tell me about yourself

✅ Explain your projects

✅ Describe your internship

✅ What are your technical skills?

✅ Why should we hire you?

✅ Explain your RAG system
""")

    st.markdown("---")

    st.subheader("⚙️ Tech Stack")

    st.markdown("""
🟣 FastAPI

🟢 Streamlit

🔵 ChromaDB

🟠 Sentence Transformers

🟡 Groq Llama 3.3

⚫ Railway
""")

    st.markdown("---")

    st.success(
        "✨ Every response is generated using Riya's actual resume and GitHub repositories."
    )

    st.caption(
        "Built with ❤️ by Riya Shah"
    )

# ==================================================
# HEADER
# ==================================================

st.markdown("""
<div class="hero">

<div style="font-size:70px;">
🤖
</div>

<div class="hero-title">
Riya Shah AI
</div>

<br>

<div class="hero-sub">

Hi! I'm Riya's AI representative.

I've been trained on her resume,
GitHub repositories, technical projects,
and professional experience.

Ask me anything and I'll answer using
real information from her portfolio.

</div>

</div>
""", unsafe_allow_html=True)



# ==================================================
# SESSION STATE
# ==================================================

if "messages" not in st.session_state:
    st.session_state["messages"] = []

def ask_ai(question):

    st.session_state["messages"].append(
        {
            "role": "user",
            "content": question
        }
    )

    ...

# ==================================================
# SUGGESTED QUESTIONS
# ==================================================


if len(st.session_state["messages"]) == 0:

    st.markdown("### ✨ Popular Questions")

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "👋 Tell me about yourself",
            use_container_width=True,
            key="p1"
        ):
            ask_ai(
                "Tell me about yourself."
            )

        if st.button(
            "🚀 What projects have you built?",
            use_container_width=True,
            key="p2"
        ):
            ask_ai(
                "What projects have you built?"
            )

        if st.button(
            "💼 Describe your internship",
            use_container_width=True,
            key="p3"
        ):
            ask_ai(
                "Describe your internship experience."
            )

        if st.button(
            "🤖 What AI technologies do you use?",
            use_container_width=True,
            key="p4"
        ):
            ask_ai(
                "What AI technologies do you use?"
            )

    with c2:

        if st.button(
            "☁️ Explain your cloud experience",
            use_container_width=True,
            key="p5"
        ):
            ask_ai(
                "Explain your cloud experience."
            )

        if st.button(
            "📂 Tell me about your GitHub",
            use_container_width=True,
            key="p6"
        ):
            ask_ai(
                "Tell me about your GitHub projects."
            )

        if st.button(
            "🧠 What are your strongest skills?",
            use_container_width=True,
            key="p7"
        ):
            ask_ai(
                "What are your strongest skills?"
            )

        if st.button(
            "🎯 Why should I hire you?",
            use_container_width=True,
            key="p8"
        ):
            ask_ai(
                "Why should I hire you?"
            )



# ==================================================
# DISPLAY CHAT HISTORY
# ==================================================

for message in st.session_state["messages"]:

    with st.chat_message(
        message["role"]
    ):
        st.markdown(
            message["content"]
        )

# ==================================================
# CHAT INPUT
# ==================================================

question = st.chat_input(
    "Ask me anything..."
)

if question:

    st.session_state["messages"].append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner(
            "Thinking..."
        ):

            try:

                response = requests.post(
                    API_URL,
                    json={
                        "question": question
                    },
                    timeout=90
                )

                answer = response.json().get(
                    "answer",
                    "Sorry, I couldn't generate a response."
                )

            except Exception:

                answer = """
⚠️ Unable to connect to the backend.

Please make sure the FastAPI service
is running on Railway.
"""

            st.markdown(answer)

    st.session_state["messages"].append(
        {
            "role": "assistant",
            "content": answer
        }
    )

# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.markdown("""
<div class="footer">

🧠 AI Persona powered by Retrieval-Augmented Generation

Resume • GitHub • Embeddings • ChromaDB • Groq • Railway

</div>
""", unsafe_allow_html=True)
