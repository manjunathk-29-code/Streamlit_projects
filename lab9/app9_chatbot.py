import streamlit as st
import time
from google import genai

# Page title
st.title("Gemini Chatbot")

# Connect to Gemini API
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Only ONE chat input
prompt = st.chat_input("Type your message...", key="chat_input_main")

if prompt:
    # Save and display user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    # Generate Gemini response
    
    with st.chat_message("assistant"):
        with st.spinner("Assistant is typing..."):
            try:
                response = client.interactions.create(
                    model="gemini-3.8-flash",
                    input=prompt
                )
                reply = response.output_text or "No response received."

            except Exception as e:
                reply = f"Sorry, an error occurred: {e}"

        st.write(reply)


    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Download chat history
if st.session_state.messages:
    chat_text = "\n".join(
        f"{msg['role']}: {msg['content']}"
        for msg in st.session_state.messages
    )

    st.download_button(
        label="Download Chat",
        data=chat_text,
        file_name="chat_history.txt",
        mime="text/plain"
    )



import time

if prompt:
    # Append user message here

    with st.spinner("Assistant is typing..."):
        time.sleep(1)
        reply = "Your reply here..."


import streamlit as st
from google import genai

api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

if prompt:
    with st.chat_message("user"):
        st.write(prompt)

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        with st.chat_message("assistant"):
            st.write(response.text)

    except Exception as e:
        st.error(f"Something went wrong: {e}")

