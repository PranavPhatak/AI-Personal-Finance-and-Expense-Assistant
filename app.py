import time
import streamlit as st
from agent import get_agent

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("💰 AI Personal Finance Assistant")
agent = get_agent()

for message in st.session_state.chat_history:
    role = message["role"]
    content = message["content"]
    st.chat_message(role).markdown(content)

query = st.chat_input("Ask me about your finances...")

if query:
    st.session_state.chat_history.append({"role":"user", "content":query})
    st.chat_message("user").markdown(query)

    with st.chat_message("ai"):
        placeholder = st.empty()
        status = st.empty()
        full_response = ""
        status.markdown("🔄 Processing your query...")
        response_started = False
        for chunk in agent.stream(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": query
                    }
                ]
            },
            {
                "configurable": {
                    "thread_id": "finance_agent"
                }
            }, stream_mode="messages"
        ):
            message_chunk, metadata = chunk
            if message_chunk.type == "AIMessageChunk" and not message_chunk.tool_calls:
                if message_chunk.content:
                    if not response_started:
                        status.empty()
                        response_started = True
                    content = message_chunk.content
                    full_response += content
                    placeholder.markdown(full_response)
                    time.sleep(0.03)
            st.session_state.chat_history.append({"role":"ai", "content":full_response})
        
