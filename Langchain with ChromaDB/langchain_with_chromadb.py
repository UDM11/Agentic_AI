import os
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.memory import VectorStoreRetrieverMemory

# Load API key
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Configure OpenRouter-compatible embeddings
embeddings_model = OpenAIEmbeddings(
    model="text-embedding-3-small",   # You can switch to text-embedding-3-large if needed
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=API_KEY
)

# Example documents
texts = [
    "Langchain is a framework for building AI applications.",
    "ChromaDB is a lightweight vector database.",
    "Vector databases are used for semantic search.",
    "Agents can store conversation history in a vector store."
]
ids = ["1", "2", "3", "4"]

# Create vector store from texts
vector_store = Chroma.from_texts(
    texts,
    embeddings_model,
    ids=ids,
    collection_name="my_collection"
)

# Query example
query_text = "Tell me about vector databases."
results = vector_store.similarity_search(query_text, k=2)

print("Query Results:")
for i, doc in enumerate(results, 1):
    print(f"{i}. {doc.page_content}")

# Integrate with LangChain memory
memory = VectorStoreRetrieverMemory(
    retriever=vector_store.as_retriever()
)

# Save a message to memory
memory.save_context(
    {"input": "Explain ChromaDB"},
    {"output": "ChromaDB stores embeddings."}
)

# Retrieve semantically
retrieved = memory.load_memory_variables({"input": "Tell me about vector databases"})

print("\nRetrieved from Memory:")
print(retrieved)
