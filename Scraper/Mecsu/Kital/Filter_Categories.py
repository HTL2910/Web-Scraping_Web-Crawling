import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pandastable import Table, TableModel

class DataFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng Dụng Lọc Dữ Liệu")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")
        
        self.data = None
        self.setup_ui()
        
    def setup_ui(self):
        # Frame chính
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame trên cùng cho việc tải file và tìm kiếm
        top_frame = ttk.LabelFrame(main_frame, text="Tùy chọn lọc dữ liệu", padding=10)
        top_frame.pack(fill=tk.X, pady=5)
        
        # Nút tải file
        self.load_btn = ttk.Button(top_frame, text="Tải File Excel", command=self.load_excel)
        self.load_btn.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        # Hiển thị đường dẫn file
        self.file_path_var = tk.StringVar()
        self.file_path_var.set("Chưa có file nào được chọn")
        file_path_label = ttk.Label(top_frame, textvariable=self.file_path_var)
        file_path_label.grid(row=0, column=1, columnspan=4, padx=5, pady=5, sticky="w")
        
        # Frame cho tìm kiếm văn bản
        text_search_frame = ttk.LabelFrame(top_frame, text="Tìm kiếm theo văn bản", padding=5)
        text_search_frame.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky="ew")
        
        # Nhãn tìm kiếm
        search_label = ttk.Label(text_search_frame, text="Nhập từ khóa tìm kiếm:")
        search_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        # Ô nhập từ khóa tìm kiếm
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(text_search_frame, textvariable=self.search_var, width=40)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Combobox chọn cột tìm kiếm
        column_label = ttk.Label(text_search_frame, text="Chọn cột cần tìm:")
        column_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        self.column_var = tk.StringVar()
        self.column_combo = ttk.Combobox(text_search_frame, textvariable=self.column_var, state="readonly", width=20)
        self.column_combo.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        self.column_combo.bind("<<ComboboxSelected>>", self.update_unique_values)
        
        # Nút tìm kiếm
        self.search_btn = ttk.Button(text_search_frame, text="Tìm Kiếm", command=self.filter_data_by_text)
        self.search_btn.grid(row=0, column=4, padx=5, pady=5, sticky="w")
        
        # Frame cho tìm kiếm giá trị duy nhất
        unique_search_frame = ttk.LabelFrame(top_frame, text="Lọc theo giá trị duy nhất", padding=5)
        unique_search_frame.grid(row=2, column=0, columnspan=5, padx=5, pady=5, sticky="ew")
        
        # Combobox chọn cột để lấy giá trị duy nhất
        unique_column_label = ttk.Label(unique_search_frame, text="Chọn cột:")
        unique_column_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.unique_column_var = tk.StringVar()
        self.unique_column_combo = ttk.Combobox(unique_search_frame, textvariable=self.unique_column_var, state="readonly", width=20)
        self.unique_column_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.unique_column_combo.bind("<<ComboboxSelected>>", self.update_unique_values)
        
        # Combobox chọn giá trị duy nhất
        unique_value_label = ttk.Label(unique_search_frame, text="Chọn giá trị:")
        unique_value_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        self.unique_value_var = tk.StringVar()
        self.unique_value_combo = ttk.Combobox(unique_search_frame, textvariable=self.unique_value_var, state="readonly", width=30)
        self.unique_value_combo.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        # Nút lọc theo giá trị duy nhất
        self.filter_unique_btn = ttk.Button(unique_search_frame, text="Lọc Dữ Liệu", command=self.filter_data_by_unique)
        self.filter_unique_btn.grid(row=0, column=4, padx=5, pady=5, sticky="w")
        
        # Frame hiển thị kết quả
        self.result_frame = ttk.LabelFrame(main_frame, text="Kết quả", padding=10)
        self.result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Tab control để hiển thị dữ liệu gốc và dữ liệu đã lọc
        self.tab_control = ttk.Notebook(self.result_frame)
        
        self.original_tab = ttk.Frame(self.tab_control)
        self.filtered_tab = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.original_tab, text="Dữ liệu gốc")
        self.tab_control.add(self.filtered_tab, text="Dữ liệu đã lọc")
        
        self.tab_control.pack(fill=tk.BOTH, expand=True)
        
        # Frame dưới cùng cho các nút
        bottom_frame = ttk.Frame(main_frame, padding=10)
        bottom_frame.pack(fill=tk.X, pady=5)
        
        # Nút xuất file kết quả
        self.export_btn = ttk.Button(bottom_frame, text="Xuất kết quả tìm kiếm", command=self.export_results)
        self.export_btn.pack(side=tk.RIGHT, padx=5)
        
        # Nút làm mới
        self.reset_btn = ttk.Button(bottom_frame, text="Làm mới bộ lọc", command=self.reset_filters)
        self.reset_btn.pack(side=tk.RIGHT, padx=5)
        
        # Khởi tạo biến cho bảng
        self.original_table = None
        self.filtered_table = None
        
        # Thông báo trạng thái
        self.status_var = tk.StringVar()
        self.status_var.set("Sẵn sàng")
        status_label = ttk.Label(bottom_frame, textvariable=self.status_var)
        status_label.pack(side=tk.LEFT, padx=5)
        
    def load_excel(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx;*.xls"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.file_path_var.set(file_path)
                self.data = pd.read_excel(file_path)
                self.status_var.set(f"Đã tải file với {len(self.data)} dòng và {len(self.data.columns)} cột")
                
                # Cập nhật danh sách cột cho cả hai combobox
                column_list = list(self.data.columns)
                self.column_combo["values"] = column_list
                self.unique_column_combo["values"] = column_list
                
                # Tự động chọn cột 'Description' nếu có
                if 'Description' in self.data.columns:
                    self.column_combo.set('Description')
                    self.unique_column_combo.set('Description')
                    self.update_unique_values(None)  # Cập nhật giá trị duy nhất ban đầu
                else:
                    self.column_combo.current(0)
                    self.unique_column_combo.current(0)
                    self.update_unique_values(None)  # Cập nhật giá trị duy nhất ban đầu
                
                # Hiển thị dữ liệu gốc
                self.show_original_data()
                
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể đọc file: {str(e)}")
    
    def update_unique_values(self, event):
        """Cập nhật danh sách giá trị duy nhất cho combobox khi thay đổi cột"""
        if self.data is None:
            return
        
        selected_column = self.unique_column_var.get()
        if not selected_column:
            return
            
        try:
            # Lấy danh sách các giá trị duy nhất từ cột đã chọn
            unique_values = self.data[selected_column].dropna().unique().tolist()
            
            # Sắp xếp các giá trị
            try:
                unique_values.sort()
            except:
                # Nếu không thể sắp xếp (các kiểu dữ liệu khác nhau), bỏ qua
                pass
                
            # Chuyển các giá trị thành chuỗi để hiển thị trong combobox
            unique_str_values = [str(val) for val in unique_values]
            
            # Thêm tùy chọn "Tất cả" vào đầu danh sách
            unique_str_values.insert(0, "-- Tất cả --")
            
            # Cập nhật combobox giá trị duy nhất
            self.unique_value_combo["values"] = unique_str_values
            self.unique_value_combo.current(0)  # Chọn "Tất cả" mặc định
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lấy giá trị duy nhất: {str(e)}")
    
    def show_original_data(self):
        # Xóa bảng cũ nếu có
        if self.original_table:
            self.original_table.destroy()
        
        # Tạo bảng mới với dữ liệu gốc
        frame = ttk.Frame(self.original_tab)
        frame.pack(fill=tk.BOTH, expand=True)
        
        self.original_table = Table(frame, dataframe=self.data, showtoolbar=True, showstatusbar=True)
        self.original_table.show()
    
    def filter_data_by_text(self):
        """Lọc dữ liệu theo từ khóa tìm kiếm"""
        if self.data is None:
            messagebox.showwarning("Cảnh báo", "Vui lòng tải file dữ liệu trước!")
            return
        
        search_term = self.search_var.get()
        column = self.column_var.get()
        
        if not search_term:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa tìm kiếm!")
            return
        
        if not column:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn cột cần tìm!")
            return
        
        # Lọc dữ liệu
        try:
            filtered_data = self.data[self.data[column].astype(str).str.contains(search_term, case=False, na=False)]
            self.filtered_data = filtered_data
            
            # Cập nhật thông báo trạng thái
            self.status_var.set(f"Tìm thấy {len(filtered_data)} kết quả theo từ khóa '{search_term}' trong cột '{column}'")
            
            # Hiển thị dữ liệu đã lọc
            self.show_filtered_data(filtered_data)
            
            # Chuyển sang tab dữ liệu đã lọc
            self.tab_control.select(1)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lọc dữ liệu: {str(e)}")
    
    def filter_data_by_unique(self):
        """Lọc dữ liệu theo giá trị duy nhất đã chọn"""
        if self.data is None:
            messagebox.showwarning("Cảnh báo", "Vui lòng tải file dữ liệu trước!")
            return
        
        selected_column = self.unique_column_var.get()
        selected_value = self.unique_value_var.get()
        
        if not selected_column:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn cột cần lọc!")
            return
        
        if not selected_value or selected_value == "-- Tất cả --":
            # Nếu chọn "Tất cả", hiển thị tất cả dữ liệu
            self.filtered_data = self.data.copy()
            self.status_var.set(f"Hiển thị tất cả {len(self.filtered_data)} dòng dữ liệu")
        else:
            # Lọc dữ liệu theo giá trị đã chọn
            try:
                # Lọc chính xác theo giá trị (không phải tìm kiếm một phần)
                # Xử lý các kiểu dữ liệu khác nhau 
                column_type = self.data[selected_column].dtype
                
                if column_type == np.float64 or column_type == np.int64:
                    # Nếu là số, chuyển giá trị đã chọn thành số
                    try:
                        if '.' in selected_value:
                            numeric_value = float(selected_value)
                        else:
                            numeric_value = int(selected_value)
                        self.filtered_data = self.data[self.data[selected_column] == numeric_value]
                    except ValueError:
                        self.filtered_data = self.data[self.data[selected_column].astype(str) == selected_value]
                else:
                    # Nếu không phải số, so sánh chuỗi
                    self.filtered_data = self.data[self.data[selected_column].astype(str) == selected_value]
                
                self.status_var.set(f"Tìm thấy {len(self.filtered_data)} dòng với giá trị '{selected_value}' trong cột '{selected_column}'")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi lọc dữ liệu: {str(e)}")
                return
        
        # Hiển thị dữ liệu đã lọc
        self.show_filtered_data(self.filtered_data)
        
        # Chuyển sang tab dữ liệu đã lọc
        self.tab_control.select(1)
    
    def show_filtered_data(self, filtered_data):
        # Xóa bảng cũ nếu có
        if self.filtered_table:
            self.filtered_table.destroy()
        
        # Tạo bảng mới với dữ liệu đã lọc
        frame = ttk.Frame(self.filtered_tab)
        frame.pack(fill=tk.BOTH, expand=True)
        
        if len(filtered_data) > 0:
            self.filtered_table = Table(frame, dataframe=filtered_data, showtoolbar=True, showstatusbar=True)
            self.filtered_table.show()
        else:
            # Hiển thị thông báo nếu không có kết quả
            no_results_label = ttk.Label(frame, text="Không tìm thấy kết quả nào phù hợp!")
            no_results_label.pack(pady=20)
    
    def reset_filters(self):
        """Đặt lại tất cả các bộ lọc và hiển thị dữ liệu gốc"""
        if self.data is None:
            return
            
        # Đặt lại các trường nhập liệu
        self.search_var.set("")
        self.unique_value_combo.current(0)  # Chọn "Tất cả"
        
        # Hiển thị lại dữ liệu gốc trong tab đã lọc
        self.filtered_data = self.data.copy()
        self.show_filtered_data(self.filtered_data)
        
        self.status_var.set(f"Đã làm mới bộ lọc. Hiển thị tất cả {len(self.data)} dòng dữ liệu.")
    
    def export_results(self):
        if not hasattr(self, 'filtered_data') or self.filtered_data is None or len(self.filtered_data) == 0:
            messagebox.showwarning("Cảnh báo", "Không có dữ liệu để xuất!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    self.filtered_data.to_csv(file_path, index=False)
                else:
                    self.filtered_data.to_excel(file_path, index=False)
                
                messagebox.showinfo("Thành công", f"Đã xuất dữ liệu thành công vào file:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xuất dữ liệu: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataFilterApp(root)
    root.mainloop()