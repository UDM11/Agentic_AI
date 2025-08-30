from langchain.agents import initialize_agent, Tool
from langchain_openai import ChatOpenAI

import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# define tools
def calculator_tool(expression: str) -> str:
    return str(eval(expression))

def weather_tool(city: str) -> str:
    return f"Weather in {city} is 25°C and sunny"


calculator = Tool(
    name = "calculator",
    func = calculator_tool,
    description = "Evaluates mahtmatical expressions."
)


weather = Tool(
    name = "weather",
    func = weather_tool,
    description = "Gets current weather for a city."
)

# Load LLM 
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    openai_api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# initialize agent with reasoning ability
agent = initialize_agent(
    tools = [calculator, weather],
    llm = llm,
    agent = "zero-shot-react-description",
    verbose = True
)

# Run a multi step query 
response = agent.invoke({"input": "what us the weather in Kathmandu and calcualte 15 multiplied by 3 plus 10?"})
print("Final Output: ", response)