from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# Initialize embeddings (via OpenRouter)
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# Load documents
loader = TextLoader("knowledge_base.txt", encoding="utf-8")
documents = loader.load()

# Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = splitter.split_documents(documents)

# Create or load Chroma index
persist_dir = "rag_index_chroma"
vectorstore = Chroma.from_documents(docs, embeddings, persist_directory=persist_dir)

# Build RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(
        model_name="deepseek/deepseek-chat-v3.1",
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=0,
        max_tokens=1000
    ),
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# Query
response = qa_chain.invoke({"query": "What is the latest AI trends?"})
print("RAG Response:\n", response['result'])
