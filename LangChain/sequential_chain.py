from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Define chat LLM
llm = ChatOpenAI(
    model_name="deepseek/deepseek-chat-v3.1",
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
    max_tokens=500
)

# Summarize text prompt
summarize_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("You are a helpful assistant."),
    HumanMessagePromptTemplate.from_template(
        "Summarize the following text in one sentence:\n\n{text}"
    )
])
summarize_chain = LLMChain(llm=llm, prompt=summarize_prompt)

# Translate summary to French prompt
translate_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("You are a helpful assistant."),
    HumanMessagePromptTemplate.from_template(
        "Translate this into French:\n\n{summary}"
    )
])
translate_chain = LLMChain(llm=llm, prompt=translate_prompt)

# Sequential chain
sequential_chain = SimpleSequentialChain(
    chains=[summarize_chain, translate_chain],
    verbose=True
)

# Input text
input_text = "LangChain helps developers create powerful applications using LLMs with minimal effort."

# Run chain
result = sequential_chain.run(input_text)
print("Sequential Chain Output:\n", result)
