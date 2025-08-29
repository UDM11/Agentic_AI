from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Use ChatOpenAI for OpenRouter models
llm = ChatOpenAI(
    model_name="deepseek/deepseek-chat-v3.1",
    temperature=0,
    max_tokens=500,
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# Prompt
prompt = PromptTemplate(
    input_variables=["topic"],
    template="Write a short poem about {topic}."
)

# Chain
chain = prompt | llm

# Run
result = chain.invoke({"topic": "AI"})
print("Output:\n", result)
