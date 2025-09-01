from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

# Load documents
file_path = r"C:\Users\Asus\Desktop\Agentic AI\RAG with LangChain\knowledge_base.txt"
if not os.path.exists(file_path):
    raise FileNotFoundError(f"{file_path} not found! Make sure the file exists.")

loader = TextLoader(file_path)
documents = loader.load()

# Split documents into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
chunks = text_splitter.split_documents(documents)

# Generate embeddings
embeddings = OpenAIEmbeddings(
    gemini_api_key=GEMINI_API_KEY,
    model="gemini-embedding-001",
    base_url="https://api.generativeai.google/v1beta2"
)

# Create vector store
vectorstore = Chroma.from_documents(chunks, embeddings)

# Create RetrievalQA chain
llm = ChatOpenAI(
    model_name="deepseek/deepseek-chat-v3.1",
    openai_api_key=OPENAI_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
    max_tokens=1000
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# Ask a question
question = "What are the latest AI trends?"
response = qa_chain.run(question)
print("RAG Response:\n", response)