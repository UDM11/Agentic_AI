def calculator (a, b):
    return a * b
# Simulated agent with tool calling
user_query = "What is 12345 * 6789?"


# LLM decides: "I need the calculator tool"
result = calculator(12345, 6789)


# Agent final asnwer
print(f"The answer is {result}.")