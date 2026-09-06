from langchain.agents import create_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from database import db
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
from prompt import system_prompt
from dotenv import load_dotenv
load_dotenv()

model = ChatGroq(model="openai/gpt-oss-120b")
toolkit = SQLDatabaseToolkit(db=db, llm=model)
tools = toolkit.get_tools()

def get_agent():
    agent = create_agent(
        model = model,
        tools=tools,
        checkpointer=InMemorySaver(),
        system_prompt=system_prompt
    )
    return agent