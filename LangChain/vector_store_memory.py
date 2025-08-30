from langchain.memory import VectorStoreRetrieverMemory
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool 

import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    openai_api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# create embedding and vector store
embeddings = OpenAIEmbeddings()
texts = [
    "John, lives in kathmandu.",
    "Langchain provides  memory for agents."
    "Vector databases allow semantic search."
]
vectorstore = FAISS.from_texts(texts, embeddings)

# convert vector store to retriever memory
retriever = vectorstore.as_retriever()
memory = VectorStoreRetrieverMemory(retriever=retriever, memory_key="chat_history")


tools = []
agent = initialize_agent(
    tools = tools,
    llm = llm, 
    memory = memory,
    agent = "conversational-react-description",
    verbose = True
)

print(agent.invoke({"input": "Remember that my favorite programming language is python."}))
print(agent.invoke({"input": "where do i live?"}))
print(agent.invoke({"input": "what is my favorite programming language?"}))