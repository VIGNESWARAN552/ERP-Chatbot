import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings  # use the new recommended import
load_dotenv()

# Use your actual OpenAI API key here
openai_api_key = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Sample documents - replace with your real documents/texts
documents = [
    "This is the first document.",
    "This is the second document.",
    "This is another example document."
]

# Create FAISS vector store from documents
vector_store = FAISS.from_texts(documents, embeddings)
vector_store.save_local("faiss_index")

# Save the index locally (this creates app/faiss_index/index.faiss and metadata files)
vector_store.save_local("app/faiss_index")

print("FAISS index saved successfully!")
