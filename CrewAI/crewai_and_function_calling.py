from crewai import Agent, Task
from langchain.tools import Tool
from openai import OpenAI


import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# define a function the agent can call
def weather_tool(city: str) -> str:
    """
    Returns sumlated weahter data for a given city.
    IN a real setup, you could call a weahter API here.
    """

    fake_weather_data = {
        "Kathmandu": {"temp": "22°C", "condition": "Sunny"},
        "Pokhara": {"temp": "20°C", "condition": "Cloudy"},
        "Biratnagar": {"temp": "30°C", "condition": "Rainy"},
    }
    return fake_weather_data.get(city, {"temp": "N/A", "condition": "N/A"})


# wrap the function as a Tool
weather_tool_wrapper = Tool(
    name = "get_weather",
    func = weather_tool,
    description = "Provides current weahter informatkon for a given city."
)



# define the agent with the tool
weather_tool = Agent(
    role = "Weather Researcher",
    goal = "Provide accurate weather information on request",
    backstory = "You are a meteorologist with access to real-time weather data.",
    tools = [weather_tool_wrapper],
    llm = OpenAI(
        model_name="gpt-4o-mini",
        temperature=0.7,
        openai_api_key=API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )
)

# create a task for the agent
user_task = Task(
    input_task = "What is the weahter in Pokhara Today?"
)


# let the agent decide and act
response = weather_tool.invoke({"task": user_task})
print(response)