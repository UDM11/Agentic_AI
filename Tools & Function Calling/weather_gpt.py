import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI

# Load API keys
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Initialize OpenAI client (OpenRouter)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENAI_API_KEY
)

# Define tool GPT can call
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "Name of the city"}
                },
                "required": ["city"]
            }
        }
    }
]

# Helper function: fetch weather from OpenWeatherMap
def fetch_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        description = data['weather'][0]['description']
        temp = data['main']['temp']
        return f"The weather in {city} is {description} with a temperature of {temp}°C."
    else:
        return f"Could not fetch weather for {city}. Please check the city name."

# Interactive loop
while True:
    user_input = input("\nAsk GPT about the weather (or type 'exit' to quit): ")
    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    # Step 1: Ask GPT
    completion = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3.1",
        messages=[{"role": "user", "content": user_input}],
        tools=tools,
        max_tokens=500,
        tool_choice="required"  # ensure GPT uses the tool if possible
    )

    message = completion.choices[0].message

    # Step 2: Handle tool call if GPT triggers it
    if getattr(message, "tool_choice", None):
        tool_name = message.tool_choice.name
        arguments = json.loads(message.tool_choice.arguments)
        city = arguments.get("city")
        weather_info = fetch_weather(city)

        # Step 3: Send back to GPT for follow-up
        follow_up = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3.1",
            messages=[
                {"role": "user", "content": user_input},
                {"role": "function", "name": tool_name, "content": weather_info}
            ],
            max_tokens=500
        )
        print(follow_up.choices[0].message.content)

    else:
        # GPT didn't trigger tool → extract city manually and fetch weather
        city = user_input.strip().title()  # simple normalization
        weather_info = fetch_weather(city)
        print(weather_info)
