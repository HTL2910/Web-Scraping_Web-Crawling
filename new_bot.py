from fastapi import FastAPI
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import openai
import os
import pandas as pd

# Set API Key
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

# Load FAISS Index từ LangChain
vectorstore = FAISS.load_local("mecsu_faiss.index", OpenAIEmbeddings())
df = pd.read_csv("Mecsu_full_data.csv")

# Khởi tạo FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Chatbot RAG API is running!"}

@app.get("/search/")
def search(query: str, top_k: int = 5):
    # Tìm kiếm FAISS trong LangChain
    docs = vectorstore.similarity_search(query, k=top_k)

    # Lấy nội dung sản phẩm
    context = "\n".join([f"{doc.metadata.get('Name', 'Sản phẩm')}: {doc.page_content}" for doc in docs])

    # Dùng GPT-4 để trả lời
    llm = ChatOpenAI(model="gpt-4")
    response = llm.invoke([
        SystemMessage(content="Bạn là một chuyên gia kỹ thuật."),
        HumanMessage(content=f"Dưới đây là thông tin sản phẩm:\n{context}\n\nHãy trả lời câu hỏi: {query}")
    ])

    return {"query": query, "results": context, "llm_answer": response.content}

