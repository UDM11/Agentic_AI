from langchain.agents import initialize_agent, Tool
from langchain_openai import OpenAI
from langchain.memory import ConversationBufferMemory


import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# LLM setup
llm = OpenAI(
    model_name="deepseek/deepseek-chat-v3.1",
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
    max_tokens=500
)

# Tools
tools = [
    Tool(
        name="calculator",
        func=lambda x: str(eval(x)),
        description="Performs basic arithmetic calculations."
    ),
    Tool(
        name="Search",
        func=lambda query: f"Search result for '{query}'",
        description="Searches for information online."
    )
]

# Memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Initialize agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    memory=memory,
    verbose=True
)

# Run agent
response1 = agent.run("Hello, can you calculate 5 * 815?")
response2 = agent.run("Now, can you summarize what we just did?")
response3 = agent.run("Also, Search for LangChain.")

# Print outputs
print("\nStep 1:", response1)
print("Step 2:", response2)
print("Step 3:", response3)

print("\nChat History:\n", memory.buffer)
