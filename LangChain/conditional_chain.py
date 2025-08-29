from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Initialize chat LLM
llm = ChatOpenAI(
    model_name="deepseek/deepseek-chat-v3.1",
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0
)

# Positive sentiment prompt
positive_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("You are a helpful assistant."),
    HumanMessagePromptTemplate.from_template(
        "The review is positive: {review}. Write a thank you reply."
    )
])
positive_chain = positive_prompt | llm

# Negative sentiment prompt
negative_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("You are a helpful assistant."),
    HumanMessagePromptTemplate.from_template(
        "The review is negative: {review}. Write an apology reply."
    )
])
negative_chain = negative_prompt | llm

# Router function
def sentiment_router(review: str) -> str:
    if "good" in review.lower() or "great" in review.lower():
        return positive_chain.invoke({"review": review})
    else:
        return negative_chain.invoke({"review": review})

# Test
print("Conditional Chain Output (Positive): \n", sentiment_router("The service was great and fast"))
print("Conditional Chain Output (Negative): \n", sentiment_router("The service was slow and bad"))
