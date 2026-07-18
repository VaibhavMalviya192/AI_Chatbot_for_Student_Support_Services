import streamlit as st

from chatbot import get_response

st.set_page_config(
    page_title="Student Support Chatbot",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 AI Student Support Chatbot")

st.write(
    "Ask questions related to admissions, fees, hostel, exams, scholarships, library, placements, etc."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask your question...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    response = get_response(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun
