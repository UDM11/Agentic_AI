from openai import OpenAI
import json
import os
from dotenv import load_dotenv


# Load API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")




client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENAI_API_KEY
)



# Tool Definitions
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate mathematical expressions",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string"}
                },
                "required": ["expression"]
            }
        }
    }
]



# Tool Implementations
def calculator(expression):
    try:
        return str(eval(expression))
    except Exception:
        return "Error: Invalid expression."

def get_current_weather(city):
    return f"The weather in {city} is sunny with a temperature of 25°C."



# Chatbot Core
def chatbot(messages):
    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3.1",
        messages=messages,
        tools=tools,
        tool_choice="auto",       
        max_tokens=500
    )

    message = response.choices[0].message

    if message.tool_calls:
        for tool_call in message.tool_calls:
            func_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            if func_name == "calculator":
                result = calculator(arguments["expression"])
            elif func_name == "get_current_weather":
                result = get_current_weather(arguments["city"])
            else:
                result = "Function not implemented."

            # Append tool response
            messages.append(message.dict())
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

        # Continue conversation with the tool result
        return chatbot(messages)
    else:
        return message.content



# Interactive Loop
if __name__ == "__main__":
    messages = []
    print("Chatbot is ready. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        messages.append({"role": "user", "content": user_input})
        reply = chatbot(messages)
        print("Bot:", reply)
        messages.append({"role": "assistant", "content": reply})
