import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

# file path
file_path = r"C:\Users\Asus\Desktop\Agentic AI\RAG with LangChain\Knowledge_base.txt"

# Check if the file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"{file_path} not found! Make sure the file exists.")

# Load the document
loader = TextLoader(file_path)
documents = loader.load()

# Split into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)

# Print summary
print(f"Loaded {len(documents)} document(s) and split into {len(chunks)} chunks.\n")

# print chunks as a preview
for i, chunk in enumerate(chunks[:10], start=1):
    print(f"Chunk {i}")
    print(chunk.page_content)
    print()
