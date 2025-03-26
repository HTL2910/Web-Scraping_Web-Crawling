from fastapi import FastAPI, HTTPException
import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer
import requests
import threading
import os
app = FastAPI()

# Load FAISS index và dữ liệu
faiss_index_path = "D:/Python_Project/Web-Scraping_Web-Crawling/Scraper/Model/mecsu_faiss.index"
df_path = "D:/Python_Project/Web-Scraping_Web-Crawling/Scraper/Model/Mecsu_full_data.csv"

print("🔄 Đang tải FAISS index và dữ liệu...")
index = faiss.read_index(faiss_index_path)
df = pd.read_csv(df_path)

# Load model để tạo embeddings
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

@app.get("/")
def home():
    return {"message": "Chatbot RAG API is running!"}

@app.get("/search/")
def search(query: str, top_k: int = 5):
    try:
        query_embedding = model.encode([query], convert_to_numpy=True)
        D, I = index.search(query_embedding, top_k)
        
        # Lấy dữ liệu từ FAISS
        results = df.iloc[I[0]].to_dict(orient="records")

        return {"query": query, "results": results}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Hàm để nhận input từ console và gọi API
def console_input(event):
    event.wait()  # Chờ cho đến khi server đã khởi động
    while True:
        query = input("Nhập câu hỏi (hoặc 'exit' để thoát): ")
        if query.lower() == 'exit':
            break
        
        # Gọi API
        response = requests.get(f"http://127.0.0.1:8000/search/", params={"query": query, "top_k": 5})
        
        if response.status_code == 200:
            print("Kết quả:", response.json())
        else:
            print("Có lỗi xảy ra:", response.text)

if __name__ == "__main__":
    # Sử dụng threading.Event để đồng bộ hóa
    server_started = threading.Event()

    # Chạy FastAPI trong một luồng riêng
    def run_server():
        os.system("uvicorn app:app --reload")
        server_started.set()  # Đánh dấu rằng server đã khởi động

    threading.Thread(target=run_server).start()
    
    # Bắt đầu nhận input từ console
    console_input(server_started)
