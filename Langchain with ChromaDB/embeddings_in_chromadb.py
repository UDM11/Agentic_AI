texts = ["Hello world", "Hi there"]
ids = ["1", "2"]

# Define or import your embeddings model here
from langchain.embeddings import OpenAIEmbeddings
embeddings_model = OpenAIEmbeddings()

# convert texts to vectors
vectors = [embeddings_model.embed_query(text) for text in texts]


# add to chromadb 
import chromadb

client = chromadb.Client()
collection = client.create_collection(name="my_collection")

collection.add(
    documents = texts,
    embeddings = vectors,
    ids = ids
)