from crewai import Agent, Task
from langchain.tools import Tool
from openai import OpenAI

import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")


# Weather function
def weather_tool(city: str) -> dict:
    fake_weather_data = {
        "Kathmandu": {"temp": "25°C", "condition": "Sunny"},
        "Pokhara": {"temp": "22°C", "condition": "Cloudy"},
        "Biratnagar": {"temp": "28°C", "condition": "Rainy"}
    }
    return fake_weather_data.get(city, {"temp": "Unknown", "condition": "Unknown"})

# Calculator function
def calculator_tool(expression: str) -> dict:
    try:
        result = eval(expression)
        return {"expression": expression, "result": result}
    except Exception as e:
        return {"error": str(e)}

# Wrap the functions as Tools
weather_tool_wrapper = Tool(
    name="get_weather",
    func=weather_tool,
    description="Provides current weather information for a city."
)

calculator_tool_wrapper = Tool(
    name="calculate",
    func=calculator_tool,
    description="Evaluates a mathematical expression."
)


# Define the LLM
llm = OpenAI(
    model_name="gpt-4o-mini",
    temperature=0.7,
    openai_api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# Define the multi-tool agent
multi_tool_agent = Agent(
    role="Researcher Agent",
    goal="Provide accurate weather info or calculate results based on user queries",
    backstory="You are an expert researcher capable of weather analysis and calculations.",
    tools=[weather_tool_wrapper, calculator_tool_wrapper],
    llm = llm
)

# Define tasks
tasks = [
    Task(description="What's the weather in Pokhara today?", agent=multi_tool_agent),
    Task(description="Calculate 256 * 12 + 34", agent=multi_tool_agent)
]

# Run the agent on each task
for task in tasks:
    response = multi_tool_agent.run(task)
    print(response)
