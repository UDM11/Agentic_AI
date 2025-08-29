from langchain.agents import initialize_agent, Tool
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Define tools
def calculator_tool(expression: str) -> str:
    try:
        return str(eval(expression))
    except Exception:
        return "Invalid expression."

calculator = Tool(
    name="calculator",
    func=calculator_tool,
    description="Evaluates mathematical expressions."
)

def weather_tool(city: str) -> str:
    return f"Weather in {city} is 25°C and sunny"

weather = Tool(
    name="get_weather",
    func=weather_tool,
    description="Gets current weather for a city."
)

# Load LLM (Chat model, not deprecated OpenAI class)
llm = ChatOpenAI(
    model="gpt-3.5-turbo",  # or "gpt-4o-mini"
    api_key=API_KEY,
    temperature=0,
    max_tokens=500
)

# Initialize agent with tools
tools = [calculator, weather]
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

# Run queries using .invoke()
print(agent.invoke({"input": "What is the weather in Kathmandu?"}))
print(agent.invoke({"input": "What is 25 multiplied by 4 plus 10?"}))
