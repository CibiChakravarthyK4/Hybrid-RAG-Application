import streamlit as st
import requests

# Page configuration
st.set_page_config(page_title="Hybrid RAG App", page_icon="🤖", layout="centered")

# Custom CSS for distinct Left (Assistant) and Right (User) chat bubbles
st.markdown("""
<style>
    /* Default message styling */
    [data-testid="stChatMessage"] {
        padding: 1rem;
        border-radius: 0.75rem;
        margin-bottom: 0.75rem;
        display: flex;
        width: 100%;
    }
    
    /* User message styling: light blue background, content shifted right */
    [data-testid="stChatMessage"]:has(img[alt*="🧑"]) {
        background-color: #e3f2fd;
        flex-direction: row-reverse;
        text-align: right;
    }

    /* Assistant message styling: light gray background, left aligned */
    [data-testid="stChatMessage"]:has(img[alt*="🤖"]) {
        background-color: #f1f3f4;
        flex-direction: row;
        text-align: left;
    }
</style>
""", unsafe_allow_html=True)

st.title("Hybrid RAG Application")
st.write("Upload a PDF document and chat with your data.")

# Backend API URL (Docker service name or localhost)
BACKEND_URL = "http://backend:8000"

# File uploader section
uploaded_file = st.file_uploader("Upload your PDF document", type=["pdf"])

if uploaded_file is not None:
    if "uploaded_filename" not in st.session_state or st.session_state.uploaded_filename != uploaded_file.name:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
        try:
            response = requests.post(f"{BACKEND_URL}/upload", files=files)
            if response.status_code == 200:
                st.success(f"Currently chatting with: {uploaded_file.name}")
                st.session_state.uploaded_filename = uploaded_file.name
            else:
                st.error(f"Error processing file: {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the backend server.")

st.divider()

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages
for message in st.session_state.messages:
    avatar = "🧑" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Chat input widget pinned to bottom
if prompt := st.chat_input("Ask a question about your document..."):
    # Append user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(f"{BACKEND_URL}/chat", json={"question": prompt})
                if response.status_code == 200:
                    answer = response.json().get("answer", "No answer returned.")
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    error_msg = f"Error from backend: {response.text}"
                    st.error(error_msg)
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the backend server.")