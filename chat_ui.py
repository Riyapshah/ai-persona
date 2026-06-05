import streamlit as st
import requests

st.set_page_config(
    page_title="Riya Shah AI Persona",
    page_icon="🤖"
)

st.title("🤖 Riya Shah AI Persona")

st.write(
    "Ask me about Riya's background, projects, skills, or experience."
)

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):
        st.markdown(
            message["content"]
        )



question = st.chat_input(
    "Ask a question..."
)

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    try:

        response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={
                "question": question
            }
        )

        answer = response.json()[
            "answer"
        ]

    except Exception:

        answer = (
            "Unable to connect to backend."
        )

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    with st.chat_message(
        "assistant"
    ):
        st.markdown(answer)