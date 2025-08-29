from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI

import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")


# Chat LLM
llm = ChatOpenAI(
    model_name="deepseek/deepseek-chat-v3.1",
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
    max_tokens=500
)


tools = [
    Tool(
        name="calculator",
        func=lambda x: str(eval(x)),
        description="Performs basic arithmatic calculations."
    ),
    Tool(
        name = "Search",
        func = lambda query: f"Search result for '{query}'",
        description = "Searches for information on the internet."
    )
]

# Initialize agent
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)



# Run agent
query = "What is 12 * 8 and summarize the search result for LangChain?"
response = agent.invoke({"input": query})
print("\nAgent Response: \n", response)