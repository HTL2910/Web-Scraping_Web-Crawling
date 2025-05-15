import tkinter as tk
import pandas as pd
import openpyxl
from openpyxl import Workbook
from tkinter import messagebox, filedialog
from tkinter import ttk
import pandas as pd
import numpy as np
import re
from tkinter.filedialog import asksaveasfilename
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import requests
import csv
import bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas
import time
from selenium.webdriver.common.action_chains import ActionChains
import os
from tksheet import Sheet


USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
options = Options()
options.add_argument('--headless')  # Chạy không hiển thị giao diện
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument(f'user-agent={USER_AGENT}')
options.add_argument('--enable-unsafe-swiftshader')
service = Service() 
driver = webdriver.Chrome(service=service, options=options)
options.add_argument('--disable-software-rasterizer') 
action=ActionChains(driver)

USER_AGENT='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
REQUEST_HEADER={
    'User-Agent':USER_AGENT,
    'Accept-Language':'en-US,en;q=0.5',
}


loading_window = None  # Biến toàn cục để giữ cửa sổ loading
current_df = None  # Đây sẽ là nơi lưu DataFrame sau xử lý
width_member=50
height_member=50
def show_loading(message="Đang xử lý..."):
    global loading_window
    loading_window = tk.Toplevel()
    loading_window.title("Vui lòng đợi")
    loading_window.geometry("200x100")
    loading_window.resizable(False, False)
    loading_window.grab_set()
    tk.Label(loading_window, text=message, font=("Arial", 11)).pack(expand=True)
    loading_window.update()

def hide_loading():
    global loading_window
    if loading_window:
        loading_window.destroy()
        loading_window = None

def xu_ly_file():
    file_window = tk.Toplevel(root)
    file_window.title("Xử lý File Excel")
    file_window.geometry("400x400")

    tk.Label(file_window, text="Chức năng xử lý file:", font=("Arial", 12, "bold")).pack(pady=10)

    # Gộp file Excel
    tk.Button(file_window, text="Gộp File Excel", width=width_member, command=lambda: gop_file_excel(sheet_entry.get())).pack(pady=5)
    tk.Label(file_window, text="Tên Sheet để gộp (nếu có):").pack()
    sheet_entry = tk.Entry(file_window)
    sheet_entry.pack(pady=3)

    # Tách file Excel
    tk.Button(file_window, text="Tách File theo dòng", width=width_member, command=lambda: tach_file_theo_dong(int(row_entry.get()))).pack(pady=5)
    tk.Label(file_window, text="Số dòng mỗi file:").pack()
    row_entry = tk.Entry(file_window)
    row_entry.pack(pady=3)

    tk.Button(file_window, text="Tách File theo cột", width=width_member, command=lambda: tach_file_theo_cot(col_entry.get())).pack(pady=5)
    tk.Label(file_window, text="Tên cột để tách:").pack()
    col_entry = tk.Entry(file_window)
    col_entry.pack(pady=3)

    # Import / Export
    tk.Button(file_window, text="Import File", width=width_member, command=import_file).pack(pady=10)
    tk.Button(file_window, text="Export File Excel", width=width_member, command=export_file_excel).pack(pady=5)
def select_file():
    return filedialog.askopenfilenames(
        title="Chọn các file dữ liệu",
        filetypes=[
            ("Excel/CSV files", "*.xlsx *.xls *.xlsm *.csv"),
            ("All files", "*.*")
        ]
    )

def gop_file_excel(sheet_name=None):
    files = select_file()
    if not files:
        messagebox.showwarning("Không có file", "Bạn chưa chọn file nào!")
        return

    try:
        show_loading("Đang gộp file...")
        dfs = []
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext == ".csv":
                df = pd.read_csv(file)
            else:
                # với Excel: nếu có sheet_name thì đọc sheet đó, không có thì đọc sheet đầu
                df = pd.read_excel(file, sheet_name=sheet_name) if sheet_name else pd.read_excel(file)
            dfs.append(df)

        merged_df = pd.concat(dfs, ignore_index=True)
        save_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Lưu kết quả (.xlsx)"
        )
        if save_path:
            merged_df.to_excel(save_path, index=False)
            messagebox.showinfo("Gộp thành công", f"Đã lưu tại:\n{save_path}")
        hide_loading()
    except Exception as e:
        hide_loading()
        messagebox.showerror("Lỗi", f"Gộp thất bại:\n{e}")

def tach_file_theo_dong(so_dong):
    file = filedialog.askopenfilename(
        title="Chọn file Excel",
        filetypes=[("Excel files", "*.xlsx *.xls *.xlsm"), ("All files", "*.*")]
    )    
    if not file:
        messagebox.showerror('Lỗi',"Không có file nào được chọn")
        return
    try:
        df = pd.read_excel(file)

        folder = filedialog.askdirectory(title="Chọn thư mục lưu")
        if not folder:
            messagebox.showerror('Lỗi',"Không có thư mục nào được chọn")
            return

        for i in range(0, len(df), so_dong):
            chunk = df.iloc[i:i+so_dong]
            chunk.to_excel(f"{folder}/split_{i//so_dong + 1}.xlsx", index=False)

        messagebox.showinfo("Thành công", f"Đã tách theo {so_dong} dòng tại {folder}")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
def tach_file_theo_cot(col_name):
    file = filedialog.askopenfilename(
        title="Chọn file Excel",
        filetypes=[("Excel files", "*.xlsx *.xls *.xlsm"), ("All files", "*.*")]
    )       
    if not file:
        messagebox.showerror('Lỗi',"Không có file nào được chọn")
        return
    try:
        df = pd.read_excel(file)

        if col_name not in df.columns:
            messagebox.showwarning("Không tìm thấy cột", f"Cột '{col_name}' không tồn tại!")
            return

        folder = filedialog.askdirectory(title="Chọn thư mục lưu")
        if not folder:
            return

        for value, group in df.groupby(col_name):
            safe_value = str(value).replace("/", "_")
            group.to_excel(f"{folder}/split_{safe_value}.xlsx", index=False)

        messagebox.showinfo("Thành công", f"Đã tách theo cột '{col_name}' tại {folder}")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def tach_file_excel():
    file = filedialog.askopenfilename(
        title="Chọn file Excel cần tách",
        filetypes=[("Excel files", "*.xlsx *.xls *.xlsm"), ("All files", "*.*")]
    )
    if not file:
        return

    try:
        import pandas as pd
        xls = pd.ExcelFile(file)

        folder = filedialog.askdirectory(title="Chọn thư mục để lưu các file tách")
        if not folder:
            return

        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name)
            save_path = f"{folder}/{sheet_name}.xlsx"
            df.to_excel(save_path, index=False)

        messagebox.showinfo("Thành công", f"Đã tách file theo từng sheet tại:\n{folder}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Tách file thất bại:\n{str(e)}")
def import_file():
    file_path = filedialog.askopenfilename(
        title="Chọn file để import",
        filetypes=[("Excel files", "*.xlsx *.xls *.xlsm"), ("All files", "*.*")]
    )
    if not file_path:
        return

    try:
        show_loading("Đang đọc file...")
        import pandas as pd
        df = pd.read_excel(file_path)

        hide_loading()
        messagebox.showinfo("Đọc file thành công", f"Đã đọc: {file_path}\nTổng dòng: {len(df)}")

        # Tạo cửa sổ mới để hiển thị dữ liệu
        preview_window = tk.Toplevel()
        preview_window.title("Xem trước dữ liệu Excel")
        preview_window.geometry("800x400")

      
        display_df = df

        # Scrollbar
        tree_scroll = tk.Scrollbar(preview_window)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        tree = ttk.Treeview(preview_window, yscrollcommand=tree_scroll.set)
        tree.pack(expand=True, fill="both")
        tree_scroll.config(command=tree.yview)

        # Đặt cột
        tree["columns"] = list(display_df.columns)
        tree["show"] = "headings"
        for col in display_df.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=100)

        # Thêm dữ liệu
        for index, row in display_df.iterrows():
            tree.insert("", "end", values=list(row))

    except Exception as e:
        hide_loading()
        messagebox.showerror("Lỗi", f"Không thể đọc file:\n{str(e)}")
def export_file_excel():
    global current_df
    if current_df is None:
        messagebox.showwarning("Không có dữ liệu", "Chưa có dữ liệu để export.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")],  # lưu luôn dưới dạng .xlsx
        title="Lưu kết quả (.xlsx)"
    )
    if file_path:
        try:
            show_loading("Đang xuất dữ liệu...")
            current_df.to_excel(file_path, index=False)
            hide_loading()
            messagebox.showinfo("Xuất thành công", f"Đã lưu tại:\n{file_path}")
        except Exception as e:
            hide_loading()
            messagebox.showerror("Lỗi", f"Không thể export:\n{str(e)}")


def xu_ly_data():
    data_window = tk.Toplevel()
    data_window.title("Xử Lý Data")
    data_window.geometry("400x300")
    data_window.resizable(False, False)

    tk.Label(data_window, text="Chức năng xử lý dữ liệu", font=("Arial", 13, "bold")).pack(pady=10)

    btn_craw = tk.Button(data_window, text="Craw Data", width=20, command=craw_data)
    btn_translate = tk.Button(data_window, text="Translate", width=20, command=translate_data)
    btn_up_part = tk.Button(data_window, text="Up Part", width=20, command=up_part)
    btn_up_category = tk.Button(data_window, text="Up Category", width=20, command=up_category)
    btn_up_vendor = tk.Button(data_window, text="Up Vendor", width=20, command=up_vendor)

    btn_craw.pack(pady=5)
    btn_translate.pack(pady=5)
    btn_up_part.pack(pady=5)
    btn_up_category.pack(pady=5)
    btn_up_vendor.pack(pady=5)
def craw_data():
    craw_window = tk.Toplevel()
    craw_window.title("Craw Data")
    craw_window.geometry("450x350")
    craw_window.resizable(False, False)

    tk.Label(craw_window, text="Nhập thông tin để Craw dữ liệu", font=("Arial", 13, "bold")).pack(pady=10)

    # --- Input fields ---
    tk.Label(craw_window, text="URL:").pack()
    entry_url = tk.Entry(craw_window, width=50)
    entry_url.pack(pady=5)

    tk.Label(craw_window, text="Name:").pack()
    entry_name = tk.Entry(craw_window, width=50)
    entry_name.pack(pady=5)

    tk.Label(craw_window, text="Số trang (CountPage):").pack()
    entry_page = tk.Entry(craw_window, width=10)
    entry_page.pack(pady=5)

    # --- From A to B ---
    frame_index = tk.Frame(craw_window)
    frame_index.pack(pady=10)

    tk.Label(frame_index, text="Index: From").grid(row=0, column=0, padx=5)
    entry_from = tk.Entry(frame_index, width=6)
    entry_from.grid(row=0, column=1)

    tk.Label(frame_index, text="To").grid(row=0, column=2, padx=5)
    entry_to = tk.Entry(frame_index, width=6)
    entry_to.grid(row=0, column=3)

    # --- Button Craw ---
    def on_craw_click():
        url = entry_url.get().strip()
        name = entry_name.get().strip()
        count_page = entry_page.get().strip()
        from_idx = entry_from.get().strip()
        to_idx = entry_to.get().strip()

        if not url or not name or not count_page or not from_idx or not to_idx:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ các trường!")
            return

        try:
            crawDataFromWeb(url, name, int(count_page), int(from_idx), int(to_idx))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi gọi hàm cào dữ liệu:\n{e}")

    tk.Button(craw_window, text="Craw", width=15, bg="#4CAF50", fg="white", command=on_craw_click).pack(pady=10)
def get_data_from_link(url):
    if not url:
        print("Url Error")
        return None

    driver.get(url)
    time.sleep(1.5) 
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Ảnh
    img_tag = soup.find('img', class_='zoomImg')
    img_link = img_tag['src'] if img_tag else "No Image Found"

    # Tiêu đề
    title_tag = soup.find('h1', class_='product-single__title')
    title = title_tag.text.strip() if title_tag else "Không có tiêu đề"

    # Thông tin chi tiết
    product_info = soup.find('div', class_='product-single__meta')
    details = {}
    if product_info:
        for div in product_info.find_all('div'):
            text = div.text.strip()
            if text:
                parts = text.split("】")
                if len(parts) == 2:
                    key = parts[0].replace("【", "").strip()
                    value = parts[1].strip()
                    details[key] = value

    # Mô tả
    description_tag = soup.find('div', class_='product-single__description rte')
    description = description_tag.text.strip() if description_tag else " "

    # Giá
    price_tag = soup.find("span", class_='price-item price-item--regular')
    price = price_tag.text.strip() if price_tag else "None"
    time.sleep(1.5)
    return {
        "Product Name": title,
        "Image Link": img_link,
        **details,
        "Description": description,
        "Price": price
    }
def crawDataFromWeb(urls, name, count_page, from_page, to_page):
    show_loading("Đang cào dữ liệu...")

    try:
        full_data = []
        for i in range(from_page, to_page + 1):
            print(f"🔎 Đang lấy trang {i}")
            full_data.extend(get_data_from_web(urls, i))
        
        df_web = pd.DataFrame(full_data, columns=["Page Index", "Product Name", "Product Link"])
        print(df_web.head())

        product_details_list = []
        for index, row in df_web.iterrows():
            if pd.notna(row["Product Link"]):
                product_details = get_data_from_link(row["Product Link"])
                if not product_details:
                    print(f"❌ Bỏ qua dòng {index}")
                    continue
                product_details["Product Name"] = row["Product Name"]
                product_details["Product Link"] = row["Product Link"]
                product_details_list.append(product_details)
                print(f"✅ Xong dòng {index}")

        df_details = pd.DataFrame(product_details_list)

        if {"Product Name", "Product Link"} - set(df_details.columns):
            messagebox.showwarning("Thiếu dữ liệu", "Thiếu cột Product Name hoặc Product Link trong chi tiết.")
            return

        df_final = df_web.merge(df_details, on=["Product Name", "Product Link"], how="left")

        # 👉 Chọn nơi lưu file
        file_path = asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Chọn nơi lưu file kết quả",
            initialfile=f"{name}.csv"
        )

        if not file_path:
            hide_loading()
            messagebox.showinfo("Hủy lưu", "Bạn đã hủy thao tác lưu file.")
            return

        df_final.to_csv(file_path, index=False, encoding="utf-8-sig")
        global current_df
        current_df = df_final

        hide_loading()
        messagebox.showinfo("Thành công", f"Đã lưu {len(df_web)} sản phẩm vào:\n{file_path}")

    except Exception as e:
        hide_loading()
        messagebox.showerror("Lỗi", f"Cào dữ liệu thất bại: {str(e)}")
def get_data_from_web(base_url, index):
    url = f"{base_url}&page={index}"
    driver.get(url)
    time.sleep(1.5)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    data_web = []
    products = soup.findAll('div', attrs={'class': 'spf-col-xl-2 spf-col-lg-3 spf-col-md-3 spf-col-sm-3 spf-col-6'})
    for product in products:
        name_tag = product.find("div", class_="h4 spf-product-card__title").find("a")
        name = name_tag.text.strip() if name_tag else "Không có tên"
        link = "https://kital-tools.com" + name_tag["href"] if name_tag else "Không có link"
        data_web.append([index, name, link])
    return data_web

def translate_data():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv")])
    if not file_path:
        messagebox.showerror("Lỗi", "Không có file được chọn.")
        return

    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
    except Exception as e:
        messagebox.showerror("Lỗi đọc file", str(e))
        return

    # Khởi tạo giao diện xử lý dữ liệu
    window = tk.Toplevel()
    window.title("Translate Data")
    window.geometry("1200x600")

    original_df = df.copy()
    result_df = df.copy()

    selected_column = tk.StringVar()
    split_direction = tk.StringVar(value="before")
    index_var = tk.IntVar(value=1)

    # --- Step 2: Chọn cột ---
    frame_buttons = tk.Frame(window)
    frame_buttons.pack(pady=10, fill="x")

    tk.Label(frame_buttons, text="Chọn cột làm FullName:").pack(anchor="w")

    for col in df.columns:
        btn = tk.Radiobutton(frame_buttons, text=col, variable=selected_column, value=col)
        btn.pack(side="left")

    # --- Step 3: Các tuỳ chọn phân tách ---
    options_frame = tk.Frame(window)
    options_frame.pack(pady=10)

    tk.Label(options_frame, text="Brand:").grid(row=0, column=0, padx=5)
    tk.Entry(options_frame, textvariable=index_var, width=5).grid(row=0, column=1, padx=5)

    tk.Radiobutton(options_frame, text="Trước", variable=split_direction, value="before").grid(row=0, column=2)
    tk.Radiobutton(options_frame, text="Sau", variable=split_direction, value="after").grid(row=0, column=3)

    # --- Treeview with Scrollbars ---
    tree_frame = tk.Frame(window)
    tree_frame.pack(fill="both", expand=True)

    x_scroll = tk.Scrollbar(tree_frame, orient="horizontal")
    y_scroll = tk.Scrollbar(tree_frame, orient="vertical")

    tree = ttk.Treeview(tree_frame, xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)
    x_scroll.config(command=tree.xview)
    y_scroll.config(command=tree.yview)

    x_scroll.pack(side="bottom", fill="x")
    y_scroll.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)

    def show_preview():
        nonlocal result_df
        col = selected_column.get()
        idx = index_var.get()
        if col == "":
            messagebox.showwarning("Cảnh báo", "Bạn chưa chọn cột FullName.")
            return

        def extract_brand(val):
            try:
                parts = str(val).split()
                if split_direction.get() == "before":
                    return " ".join(parts[:idx])
                else:
                    return " ".join(parts[-idx:])
            except Exception:
                return ""

        result_df["Brand"] = result_df[col].apply(extract_brand)
        update_treeview(result_df)

    def update_treeview(df_view):
        tree.delete(*tree.get_children())
        tree["columns"] = list(df_view.columns)
        tree["show"] = "headings"
        for col in df_view.columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="w")
        for _, row in df_view.iterrows():
            tree.insert("", "end", values=list(row))

    def undo_changes():
        nonlocal result_df
        result_df = original_df.copy()
        update_treeview(result_df)

    def save_result():
        file_out = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                filetypes=[("Excel file", "*.xlsx")])
        if not file_out:
            return
        try:
            result_df.to_excel(file_out, index=False)
            messagebox.showinfo("Thành công", f"Đã lưu file: {file_out}")
        except Exception as e:
            messagebox.showerror("Lỗi lưu file", str(e))

    # --- Các nút thao tác ---
    btn_frame = tk.Frame(window)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Preview", command=show_preview).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Undo", command=undo_changes).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Lưu kết quả", command=save_result).pack(side="left", padx=5)

    update_treeview(result_df)

def up_part():
    messagebox.showinfo("Up Part", "Chức năng Up Part đang được xử lý...")

def up_category():
    messagebox.showinfo("Up Category", "Chức năng Up Category đang được xử lý...")

def up_vendor():
    messagebox.showinfo("Up Vendor", "Chức năng Up Vendor đang được xử lý...")

# Cửa sổ chính
root = tk.Tk()
root.title("Ứng dụng xử lý dữ liệu")
root.geometry("300x200")

tk.Label(root, text="Chọn hành động", font=("Arial", 14)).pack(pady=20)
tk.Button(root, text="Xử lý File", width=20, command=xu_ly_file).pack(pady=5)
tk.Button(root, text="Xử lý Data", width=20, command=xu_ly_data).pack(pady=5)

root.mainloop()
