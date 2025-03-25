import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse
import os
from collections import defaultdict

class WebScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Scraper Tool")
        self.root.geometry("800x600")
        
        # Danh sách lưu trữ dữ liệu
        self.data_groups = defaultdict(list)
        self.current_data = {}
        
        # URL Input
        self.url_label = ttk.Label(root, text="Nhập URL:")
        self.url_label.pack(pady=5)
        
        self.url_entry = ttk.Entry(root, width=50)
        self.url_entry.pack(pady=5)
        
        self.analyze_button = ttk.Button(root, text="Phân tích Web", command=self.analyze_web)
        self.analyze_button.pack(pady=5)
        
        # Frame cho các nút nhóm dữ liệu
        self.buttons_frame = ttk.Frame(root)
        self.buttons_frame.pack(pady=10, fill="x")
        
        # Treeview để hiển thị kết quả
        self.tree = ttk.Treeview(root, columns=("Group", "Key", "Value"), show="headings")
        self.tree.heading("Group", text="Nhóm")
        self.tree.heading("Key", text="Trường dữ liệu")
        self.tree.heading("Value", text="Giá trị")
        self.tree.pack(pady=10, fill="both", expand=True)
        
        # Nút xuất file
        self.export_button = ttk.Button(root, text="Xuất ra CSV", command=self.export_to_csv)
        self.export_button.pack(pady=5)
        self.export_button.config(state="disabled")

    def analyze_web(self):
        # Xóa các nút cũ
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
            
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Lỗi", "Vui lòng nhập URL!")
            return
            
        try:
            # Lấy nội dung web
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Tìm các nhóm dữ liệu tương tự
            self.data_groups.clear()
            
            # Ví dụ: Tìm các khối sản phẩm/bài viết phổ biến
            possible_containers = [
                ('div', {'class': 'product'}),
                ('div', {'class': 'item'}),
                ('div', {'class': 'post'}),
                ('article', {}),
                ('section', {})
            ]
            
            group_id = 1
            for tag, attrs in possible_containers:
                items = soup.find_all(tag, attrs)
                if len(items) > 1:  # Chỉ lấy nếu có nhiều mục tương tự
                    for item in items:
                        group_data = {}
                        # Tìm các thành phần bên trong
                        for element in item.find_all():
                            if element.name in ['h1', 'h2', 'h3']:
                                group_data['title'] = element.text.strip()
                            elif element.name == 'p':
                                group_data['description'] = element.text.strip()
                            elif element.name == 'img':
                                group_data['image'] = element.get('src')
                            elif element.name == 'a':
                                group_data['link'] = element.get('href')
                        
                        if group_data:
                            self.data_groups[f"Nhóm {group_id}"].append(group_data)
                    if f"Nhóm {group_id}" in self.data_groups:
                        group_id += 1
            
            # Tạo nút cho từng nhóm
            for group_name in self.data_groups.keys():
                btn = ttk.Button(self.buttons_frame,
                               text=group_name,
                               command=lambda gn=group_name: self.add_to_results(gn))
                btn.pack(side="left", padx=5)
                
            # Thêm nút cho dữ liệu tổng quan
            overview_data = {
                "Tiêu đề trang": soup.title.string if soup.title else None,
                "Tổng số nhóm": len(self.data_groups)
            }
            btn = ttk.Button(self.buttons_frame,
                           text="Tổng quan",
                           command=lambda: self.add_to_results("Tổng quan", overview_data))
            btn.pack(side="left", padx=5)
            
            self.export_button.config(state="normal")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể phân tích URL: {str(e)}")

    def add_to_results(self, group_name, data=None):
        # Xóa dữ liệu cũ trong treeview
        self.tree.delete(*self.tree.get_children())
        
        # Thêm dữ liệu mới
        if data:  # Trường hợp dữ liệu tổng quan
            self.current_data[group_name] = data
        else:  # Trường hợp nhóm dữ liệu
            self.current_data[group_name] = self.data_groups[group_name]
        
        # Hiển thị tất cả dữ liệu hiện tại
        for group, items in self.current_data.items():
            if isinstance(items, dict):  # Dữ liệu tổng quan
                for key, value in items.items():
                    self.tree.insert("", "end", values=(group, key, value))
            else:  # Dữ liệu nhóm
                for i, item in enumerate(items):
                    for key, value in item.items():
                        self.tree.insert("", "end", values=(f"{group} - Mục {i+1}", key, value))

    def export_to_csv(self):
        if not self.current_data:
            messagebox.showwarning("Cảnh báo", "Không có dữ liệu để xuất!")
            return
            
        # Chuẩn bị dữ liệu cho DataFrame
        export_data = []
        for group, items in self.current_data.items():
            if isinstance(items, dict):  # Dữ liệu tổng quan
                export_data.append({
                    'Group': group,
                    'Key': list(items.keys())[0],
                    'Value': list(items.values())[0]
                })
            else:  # Dữ liệu nhóm
                for i, item in enumerate(items):
                    for key, value in item.items():
                        export_data.append({
                            'Group': f"{group} - Mục {i+1}",
                            'Key': key,
                            'Value': value
                        })
        
        # Tạo DataFrame
        df = pd.DataFrame(export_data)
        
        # Lấy tên file từ URL
        url = self.url_entry.get()
        domain = urlparse(url).netloc
        filename = f"{domain}_grouped_data.csv"
        
        try:
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            messagebox.showinfo("Thành công", f"Đã xuất dữ liệu ra file: {filename}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất file: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WebScraperApp(root)
    root.mainloop()