# Load FAISS index và dữ liệu
# faiss_index_path = "D:/Python_Project/Web-Scraping_Web-Crawling/Scraper/Model/mecsu_faiss.index"
# df_path = "D:/Python_Project/Web-Scraping_Web-Crawling/Scraper/Model/Mecsu_full_data.csv"

import faiss
import json
import numpy as np
import pandas as pd
import streamlit as st
from sentence_transformers import SentenceTransformer


# Load FAISS Index
index = faiss.read_index("D:\Python_Project\Web-Scraping_Web-Crawling\Scraper\Model\mecsu_faiss.index")

# Load metadata
with open("D:\Python_Project\Web-Scraping_Web-Crawling\Scraper\Model\mecsu_metadata.json", "r") as f:
    metadata = json.load(f)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Hàm tìm kiếm sản phẩm
def search_product(query, top_k=5):
    query_embedding = model.encode(query).astype(np.float32).reshape(1, -1)
    distances, indices = index.search(query_embedding, top_k)
    
    results = []
    for idx in indices[0]:
        if idx < len(metadata):
            results.append(metadata[idx])
    
    return results

# Giao diện Streamlit
st.title("🔍 Tìm kiếm sản phẩm bằng FAISS")

query = st.text_input("Nhập từ khóa tìm kiếm:")

if st.button("Tìm kiếm"):
    if query:
        results = search_product(query)
        if results:
            st.write("### Kết quả tìm kiếm:")
            for result in results:
                st.write(f"- **Mã sản phẩm**: {result['part_id']}")
                st.write(f"  🔗 [Link sản phẩm]({result['link']})")
                st.write(f"  💰 Giá: {result['price']} VND")
                st.write("---")
        else:
            st.write("Không tìm thấy sản phẩm phù hợp!")