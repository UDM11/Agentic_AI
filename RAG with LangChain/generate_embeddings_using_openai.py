import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings




# Load API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


if not OPENAI_API_KEY:
    raise ValueError("Please set your OPENAI_API_KEY environment variable.")


# load the text file
file_path = r"C:\Users\Asus\Desktop\Agentic AI\RAG with LangChain\Knowledge_base.txt"
if not os.path.exists(file_path):
    raise FileNotFoundError(f"{file_path} not found! Make sure the file exists.")


loader = TextLoader(file_path)
documents = loader.load()

# split the text into manageable chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)

# generate embeddings using openai
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small", 
    openai_api_key=OPENAI_API_KEY,
    base_url="https://openrouter.ai/api/v1" 
)


# store embeddings in chroma vector database
vectorestore = Chroma.from_documents(chunks, embeddings)
print("Embeddings generated and stored in Chroma vector database.")