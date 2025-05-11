import pandas as pd
import requests
import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
from io import BytesIO

# Giao diện chính
root = tk.Tk()
root.title("Image Downloader Tool")

file_path = ""
save_dir = ""
df = None
selected_column = None

# Load Excel file và đọc các cột
def load_file():
    global df, file_path
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if file_path:
        df = pd.read_excel(file_path)
        if 'link' not in df.columns:
            messagebox.showerror("Error", "Không tìm thấy cột 'link' trong file!")
            return
        update_column_buttons()
        status_label.config(text=f"Đã chọn file: {file_path}")

# Cập nhật danh sách các cột để chọn làm tên ảnh
column_buttons_frame = None
def update_column_buttons():
    global column_buttons_frame
    if column_buttons_frame:
        column_buttons_frame.destroy()

    column_buttons_frame = tk.Frame(root)
    column_buttons_frame.pack(pady=5)
    tk.Label(column_buttons_frame, text="Chọn cột dùng để đặt tên ảnh:").pack()

    for col in df.columns:
        btn = tk.Button(column_buttons_frame, text=col, command=lambda c=col: select_column(c))
        btn.pack(side=tk.LEFT, padx=2)

# Xử lý khi chọn cột đặt tên ảnh
preview_name = tk.StringVar()
def select_column(col):
    global selected_column
    selected_column = col
    preview = df[col].iloc[0]
    preview_name.set(f"Tên ảnh mẫu: {preview}.jpg")

# Chọn thư mục lưu ảnh
def choose_save_folder():
    global save_dir
    save_dir = filedialog.askdirectory()
    if save_dir:
        status_label.config(text=f"Ảnh sẽ lưu tại: {save_dir}")

# Tải ảnh
image_index = 1

def download_images():
    global image_index
    if df is None or selected_column is None:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn file và cột đặt tên ảnh trước!")
        return

    for i, row in df.iterrows():
        try:
            img_url = row['link']
            if pd.isna(img_url):
                continue

            response = requests.get(img_url, timeout=10)
            if response.status_code == 200:
                image_data = BytesIO(response.content)
                ext = img_url.split(".")[-1].split("?")[0]  # Lấy phần mở rộng
                
                # Lấy tên từ cột được chọn
                name_raw = str(row.get(selected_column, f"image_{image_index}"))
                name = name_raw.replace("/", "_").replace("\\", "_").replace(" ", "_")
                filename = os.path.join(save_dir, f"{name}.{ext}")

                with open(filename, 'wb') as f:
                    f.write(response.content)

                image_index += 1
        except Exception as e:
            print(f"Lỗi tải ảnh từ {row['link']}: {e}")

    messagebox.showinfo("Hoàn tất", f"Đã tải xong ảnh vào: {save_dir}")

# Các nút và khung giao diện
btn_load = tk.Button(root, text="Chọn file Excel", command=load_file)
btn_load.pack(pady=5)

btn_folder = tk.Button(root, text="Chọn nơi lưu ảnh", command=choose_save_folder)
btn_folder.pack(pady=5)

tk.Label(root, textvariable=preview_name, fg="blue").pack()

btn_download = tk.Button(root, text="Bắt đầu tải ảnh", command=download_images)
btn_download.pack(pady=10)

status_label = tk.Label(root, text="Chưa chọn file hoặc nơi lưu", fg="gray")
status_label.pack(pady=5)

root.mainloop()
