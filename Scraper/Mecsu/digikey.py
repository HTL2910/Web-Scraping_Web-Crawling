import os
import pandas as pd
from tkinter import Tk, filedialog

# 🟢 Chọn nhiều file Excel & CSV thông qua hộp thoại
def select_files():
    root = Tk()
    root.withdraw()  # Ẩn cửa sổ Tkinter
    file_paths = filedialog.askopenfilenames(
        title="Chọn file Excel hoặc CSV cần gộp",
        filetypes=[("Excel & CSV Files", "*.xlsx;*.xls;*.csv"), ("All Files", "*.*")]
    )
    return file_paths

# 🟢 Đọc dữ liệu từ tất cả file Excel & CSV và gộp theo header chung
def merge_files(file_paths):
    all_dfs = []  # Danh sách lưu các DataFrame
    for file in file_paths:
        try:
            if file.endswith(".xlsx") or file.endswith(".xls"):
                df = pd.read_excel(file, dtype=str, engine="openpyxl")  # Đọc file Excel
            elif file.endswith(".csv"):
                df = pd.read_csv(file, dtype=str, encoding="utf-8", on_bad_lines="skip")  # Bỏ qua dòng lỗi
            else:
                print(f"⚠️ Bỏ qua file không hỗ trợ: {file}")
                continue

            all_dfs.append(df)
            print(f"✅ Đã đọc: {file}")

        except Exception as e:
            print(f"❌ Lỗi khi đọc {file}: {e}")

    # Gộp tất cả file theo header chung
    if all_dfs:
        merged_df = pd.concat(all_dfs, ignore_index=True, join="outer")  
        return merged_df
    else:
        return None

# 🟢 Chọn file và gộp dữ liệu
file_paths = select_files()
if not file_paths:
    print("⚠️ Không có file nào được chọn.")
else:
    merged_df = merge_files(file_paths)

    # Xuất file Excel sau khi gộp
    if merged_df is not None:
        output_file = "hex__torx_keys.xlsx"
        merged_df.to_excel(output_file, index=False, engine="openpyxl")  # ✅ Fix lỗi encoding
        print(f"✅ Dữ liệu đã gộp và lưu vào: {output_file}")
    else:
        print("❌ Không có dữ liệu để gộp.")
