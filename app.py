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
        full_response = ""
        with st.spinner("Processing your query..."):
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
                }
            ):
                if "model" in chunk:
                    messages = chunk["model"].get("messages", [])

                    if messages:

                        content = messages[-1].content

                        if content:
                            full_response += content
                            placeholder.markdown(full_response)
            st.session_state.chat_history.append({"role":"ai", "content":full_response})
        
