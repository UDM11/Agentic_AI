from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.memory import ConversationBufferMemory

import os
from dotenv import load_dotenv


# Load API key
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Example tool
def weather_tool(city: str) -> str:
    return f"weather in {city} is 25°C and sunny"

weather = Tool(
    name = "get_weather",
    func = weather_tool,
    description = "Get the current weahter in a city."
)


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    openai_api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# memory
memory = ConversationBufferMemory(memory_key = "chat_history")


# Initialize vonversational agent
agent = initialize_agent(
    tools = [weather],
    llm = llm,
    agent = "conversational-react-description",
    memory = memory,
    verbose = True
)

# Run 
print(agent.invoke({"input": "what is the weather in Kathmandu?"}))
print(agent.invoke({"input": "what about in Ppokhara?"}))