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
        with st.spinner("Processing your query..."):
            response = agent.invoke({
                "messages":[
                    {
                        "role":"user",
                        "content": query
                    }
                ]
            },{"configurable":{"thread_id":"finance_agent"}}
            )
            message = response['messages'][-1].content
            st.session_state.chat_history.append({"role":"ai", "content":message})
            st.markdown(message)
