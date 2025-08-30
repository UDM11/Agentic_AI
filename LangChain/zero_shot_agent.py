from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Example tool
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

# LLM (use ChatOpenAI for chat-based models)
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    openai_api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# Initialize zero-shot agent
agent = initialize_agent(
    tools=[calculator],
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

# Run
response = agent.invoke({"input": "What is 25 multiplied by 4 plus 10?"})
print(response)
