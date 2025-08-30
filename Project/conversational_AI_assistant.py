from langchain.agents import initialize_agent, Tool
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")


def calculator_tool(expression: str) -> str:
    try:
        return str(eval(expression))
    except Exception:
        return "Invalid expression."
    

def weather_tool(city: str) -> str:
    return f"The weahter in {city} is sunny with a temperature of 25°C."

calculator = Tool(
    name = "calculator",
    func = calculator_tool,
    description = "solves math expressions."
)

weather = Tool(
    name = "weather",
    func = weather_tool,
    description = "gives weather info for a city"
)


memory = ConversationBufferMemory(memory_key="chat_history")

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    openai_api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


agent = initialize_agent(
    tools = [calculator, weather],
    llm = llm,
    agent = "conversational-react-description",
    memory = memory,
    verbose = True
)


user_input = [
    "Hi, can you tell me the weather in Pokhara?",
    "Also, calculate 15 * 3 for me.",
    "Thanks! what about the weather in kathmandu now?"
]

for user_input in user_input:
    response = agent.invoke({"input": user_input})
    print(f"User: {user_input}\nAgent: {response['output']}\n")
    