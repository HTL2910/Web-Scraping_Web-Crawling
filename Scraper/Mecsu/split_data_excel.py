import pandas as pd
import math
import os
import tkinter as tk
from tkinter import filedialog

# 📌 Bước 1: Chọn file Excel đầu vào
root = tk.Tk()
root.withdraw()  # Ẩn cửa sổ chính

file_path = filedialog.askopenfilename(title="Chọn file Excel để chia nhỏ", filetypes=[("Excel Files", "*.xlsx *.xls")])

if not file_path:
    print("❌ Không có file nào được chọn. Thoát chương trình!")
    exit()

# 📌 Bước 2: Chọn thư mục lưu file chia nhỏ
output_folder = filedialog.askdirectory(title="Chọn thư mục lưu các file chia nhỏ")

if not output_folder:
    print("❌ Không có thư mục nào được chọn. Thoát chương trình!")
    exit()

# 📌 Bước 3: Đọc file Excel vào DataFrame
df = pd.read_excel(file_path)

# 📌 Bước 4: Chia dữ liệu thành 19 phần
num_splits = 19
chunk_size = math.ceil(len(df) / num_splits)  # Chia đều số dòng

for i in range(num_splits):
    start_row = i * chunk_size
    end_row = min(start_row + chunk_size, len(df))  # Tránh vượt quá số dòng thực tế

    df_part = df.iloc[start_row:end_row]  # Cắt DataFrame
    output_file = os.path.join(output_folder, f"Mecsu_part_{i+1}.xlsx")

    df_part.to_excel(output_file, index=False)  # Lưu file Excel

    print(f"✅ Đã lưu: {output_file} ({len(df_part)} dòng)")

print("🎉 Hoàn tất chia nhỏ file Excel!")
