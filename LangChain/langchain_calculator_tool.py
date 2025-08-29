from langchain.tools import Tool


def calculator_tool(expression: str) -> str:
    try:
        return str(eval(expression))
    
    except Exception:
        return "Invalid expression."
    

calculator = Tool(
    name = "calculator",
    func = calculator_tool,
    description = "Evaluates mathematical expressions."
)


# Example usage
print(calculator_tool("2 + 2 * 3"))
print(calculator_tool("10 / 0"))
  