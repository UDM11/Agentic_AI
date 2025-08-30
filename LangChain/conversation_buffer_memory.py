from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool

import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    openai_api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# memory
memory = ConversationBufferMemory(memory_key = "chat_history")

# example agent setup
tools = []
agent = initialize_agent(
    tools = tools,
    llm = llm,
    agent = "conversational-react-description",
    memory = memory,
    verbose = True
)

# Run
print(agent.invoke({"input": "Hello, my name is John."}))
print(agent.invoke({"input": "What is my name?"}))