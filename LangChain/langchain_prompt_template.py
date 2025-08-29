from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import OpenAI

import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Define the prompt template
template = """You are an assistant that translates English to {language}.
Translate this sentence: "{sentence}" """

prompt = PromptTemplate(
    input_variables=["language", "sentence"],
    template=template
)

# Load the LLM
llm = OpenAI(
    model_name="deepseek/deepseek-chat-v3.1",
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
    max_tokens=100
)

# Create the chain
chain = LLMChain(llm=llm, prompt=prompt)

# Run the chain with inputs
result = chain.invoke({"language": "French", "sentence": "Good morning"})
print(result["text"])
