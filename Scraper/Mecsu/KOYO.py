from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv
import re
import pandas as pd
import pyperclip
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

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




def get_link_to_file(url):
    driver.get(url)
    time.sleep(1) 
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    return soup

def get_data(soup):
    page_col2 = soup.find('div', attrs={'class': 'page_col2 mt20'})
    data = {}
    dl_elements = page_col2.find_all('dl', class_='form_input conf_input')
    for dl in dl_elements:
        dt = dl.find('dt')  
        dd = dl.find('dd')  
        
        if dt and dd:
            dt_text = dt.get_text(strip=True)
            dd_text = dd.get_text(strip=True)
            value_without_unit = re.sub(r'\s*(min-1|kN|mm|,|[^0-9.\-])\s*', '', dd_text)
            try:
                value = float(value_without_unit)
                value_without_unit = str(value).rstrip('0').rstrip('.')  
            except ValueError:
                pass  
            if dt_text == 'd':
                data['d'] = value_without_unit
            elif dt_text == 'D':
                data['D'] = value_without_unit
            elif dt_text == 'B':
                data['B'] = value_without_unit
            elif dt_text == 'Basic load ratings : Cr':
                data['Cr'] = value_without_unit
            elif dt_text == 'Basic load ratings : C0r':
                data['C0r'] = value_without_unit
            elif dt_text == 'Fatigue load limit : Cu':
                data['Cu'] = value_without_unit
            elif dt_text == 'Limiting speeds(Grease lub.)':
                data['limit_speed_gr'] = value_without_unit
            elif dt_text == 'Limiting speeds(Oil lub.)':
                data['limit_speed_oil'] = value_without_unit
    
    return data
def get_data_from_url(url):
    soup=get_link_to_file(url)
    data=get_data(soup)
    return data
def copy_data():
    try:
        # Lấy tất cả dữ liệu từ bảng
        data = []
        for row in treeview.get_children():
            data.append(treeview.item(row)['values'])
        
        # Chuyển dữ liệu thành chuỗi văn bản
        text_data = ""
        for row in data:
            text_data += "\t".join([str(cell) for cell in row]) + "\n"
        
        # Sao chép vào clipboard
        pyperclip.copy(text_data)
        messagebox.showinfo("Success", "Data copied to clipboard successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to copy data: {e}")


def fetch_data():
    product_id = id_entry.get() 
    if product_id:
        data = get_data_from_url(product_id)  

        df = pd.DataFrame([data])

        for row in treeview.get_children():
            treeview.delete(row)

        for index, row in df.iterrows():
            treeview.insert("", "end", values=tuple(row))

root = tk.Tk()
root.title("Product Data Fetcher")

# Tạo input field để nhập ID
tk.Label(root, text="Enter Product URL:").grid(row=0, column=0, padx=10, pady=10)
id_entry = tk.Entry(root)
id_entry.grid(row=0, column=1, padx=10, pady=10)

# Tạo nút Fetch Data
fetch_button = tk.Button(root, text="Fetch Data", command=fetch_data)
fetch_button.grid(row=1, column=1, padx=10, pady=10)
copy_button = tk.Button(root, text="Copy Data", command=copy_data)
copy_button.grid(row=1, column=2, columnspan=3, pady=10)
columns = ['d', 'D', 'B', 'Cr', 'C0r', 'Cu', 'Limiting speed (Grease lub.)', 'Limiting speed (Oil lub.)']
treeview = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    treeview.heading(col, text=col)
    treeview.column(col, width=50, anchor="center")

treeview.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()