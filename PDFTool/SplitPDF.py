import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter

class PDFSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cắt PDF")
        self.root.geometry("400x250")

        # Label & Button chọn file PDF đầu vào
        self.label_input = tk.Label(root, text="Chọn file PDF:")
        self.label_input.pack(pady=5)

        self.btn_select_pdf = tk.Button(root, text="Chọn file", command=self.select_pdf)
        self.btn_select_pdf.pack()

        self.input_pdf = ""

        # Nhập số trang
        self.label_page1 = tk.Label(root, text="Nhập trang bắt đầu:")
        self.label_page1.pack(pady=5)

        self.entry_page1 = tk.Entry(root)
        self.entry_page1.pack()

        self.label_page2 = tk.Label(root, text="Nhập trang kết thúc:")
        self.label_page2.pack(pady=5)

        self.entry_page2 = tk.Entry(root)
        self.entry_page2.pack()

        # Nút thực hiện cắt file
        self.btn_cut_pdf = tk.Button(root, text="Cắt PDF", command=self.cut_pdf)
        self.btn_cut_pdf.pack(pady=10)

    def select_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.input_pdf = file_path
            messagebox.showinfo("Thông báo", f"Đã chọn file: {file_path}")

    def cut_pdf(self):
        if not self.input_pdf:
            messagebox.showwarning("Lỗi", "Vui lòng chọn file PDF trước!")
            return

        page1 = self.entry_page1.get()
        page2 = self.entry_page2.get()

        # Kiểm tra nhập số hợp lệ
        if not page1.isdigit() or not page2.isdigit():
            messagebox.showerror("Lỗi", "Vui lòng nhập số nguyên hợp lệ!")
            return

        page1, page2 = int(page1), int(page2)

        output_pdf = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not output_pdf:
            messagebox.showwarning("Lỗi", "Vui lòng chọn nơi lưu file PDF!")
            return

        try:
            reader = PdfReader(self.input_pdf)
            writer = PdfWriter()

            for i in range(page1 - 1, page2):  # PyPDF2 đếm trang từ 0
                writer.add_page(reader.pages[i])

            with open(output_pdf, "wb") as output_file:
                writer.write(output_file)

            messagebox.showinfo("Thành công", f"Đã cắt PDF thành công và lưu tại:\n{output_pdf}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")

# Chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = PDFSplitterApp(root)
    root.mainloop()
