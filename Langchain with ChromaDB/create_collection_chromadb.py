import chromadb
from chromadb.utils import embeddings_functions
from openai import ChatOpenAI

import os
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

client = chromadb.Client()

collection = client.create_collection(name="langchain_collection")