from langchain.vectorstores import Chroma
from langchain.memory import VectorStoreRetrieverMemory


# create or load a ChromaDB collection
collection = "my_collection"  # Replace with your actual collection name or object

# wrap chromadb collection in langchain vector store
vector_store = Chroma(collection = collection)


memory = VectorStoreRetrieverMemory(
    vectorsotre = vector_store,
    retriever = vector_store.as_retriever()
)