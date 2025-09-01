import openai
from tenacity import retry, stop_after_attempt, wait_fixed
import random
import time 
import os
from dotenv import load_dotenv


# Load API keys from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

CACHED_WEATHER = {
    "temperature": "22°C",
    "condition": "Partly Cloudy"
}


# alternate tool APIs 
def google_weather(location):
    if random.random() < 0.4:
        raise ConnectionError("Google weahter API failed!")
    return {"temperature": "25°C", "condition": "Sunny"}


# automatically retry decorator
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def call_openai(message):
    """call OpenAI API with retries"""
    return openai.ChatCompletion.create(
        model = "gpt-4o-mini",
        messages = message,
        base_url="https://openrouter.ai/api/v1",
    )


# agent tools with failbacks
def fetch_weather(location):
    """Primary tool with agent-level fallback"""
    tools = [fetch_weather_api, google_weather]

    for tool in tools:
        try:
            weather = tool(location)
            return f"Weather in {location}: {weather['temperature']}°C, {weather['condition']}"
        
        except Exception as e:
            print(f"{tool.__name__} failed: {e}")
            continue



    # use cached data as last resort
    try:
        print("Using cached weather data...")
        return f"Weather in {location}: {CACHED_WEATHER['temprature']}°C, {CACHED_WEATHER['condition']}"
    
    except Exception:
        return "Sorry,  I couldn't fetch the weather data right now."
    

# simulated primary api
def fetch_weather_api(location):
    if random.random() < 0.5:
        raise ConnectionError("Primary weather API failed!")
    return {"termprature": "20", "condition": "Cloudy"}



# agent query handling with prompt refinement
def agent_response(user_query, retry_count=0):
    """Generate agent response with retries and prompt refinement"""
    max_retries = 2
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_query}
    ]

    try:
        response = call_openai(messages)
        return response.choices[0].message.content
    except Exception as api_error:
        print(f"OpenAI API filed: {api_error}")
        if retry_count < max_retries:
            refined_query = f"Please answer this question clearly: {user_query}"
            print("Retrying with refined prompt...")
            return agent_response(refined_query, retry_count + 1)
        else:
            return "Sorry, I couldn't process your request right now."
        

# Example usage
if __name__ == "__main__":
    location = "Kathmandu"
    print(fetch_weather(location))


    user_query = "Explain Agentic AI in simple terms."
    print(agent_response(user_query))