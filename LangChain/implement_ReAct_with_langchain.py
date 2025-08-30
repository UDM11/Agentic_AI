from langchain.agents import initialize_agent, Tool
from langchain_openai import ChatOpenAI

import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# define a calculator tool
def calculator_tool(expression:str) -> str:
    try:
        return str(eval(expression))
    except Exception:
        return "Invalid expression."
    
calculator = Tool(
    name = "calculator",
    func = calculator_tool,
    description = "Useful for solving mathematical expressions."
)

# define a simple weather tool
def weather_tool(city: str) -> str:
    return f"The weather in {city} is 25°C and sunny."


weather = Tool(
    name = "weather",
    func = weather_tool,
    description = "Provides the current weather for a given city."
)

llm = ChatOpenAI(
    model = "gpt-4o-mini",
    api_key = API_KEY,
    temperature = 0,
    base_url="https://openrouter.ai/api/v1"
)

# initialize the ReAct agent
agent = initialize_agent(
    tools = [calculator, weather],
    llm = llm,
    agent = "zero-shot-react-description",
    verbose = True
)


# Run a query
response = agent.invoke(
    {
        "input": "what is the weather in kathmandu and calculate 25 * 4 + 10?"
    }
)

print(response)