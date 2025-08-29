import requests
from langchain.tools import Tool

def weather_tool(city: str) -> str:
    return f"weather in {city} is 25°C and sunny"

weather = Tool(
    name = "get_weather",
    func = weather_tool,
    description = "Gets current weather for a city."
)

# Example usage
print(weather_tool("Kathmandu"))