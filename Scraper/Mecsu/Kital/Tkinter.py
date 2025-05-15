import tkinter as tk
import tkinter.ttk as ttk

# Tạo cửa sổ chính
window = tk.Tk()
window.title("Simple Tkinter App")
window.geometry("400x300")

# Label đầu tiên
greet = tk.Label(window, text="Hi Python", foreground="green", background="black")
greet.pack(pady=5)

# Label với ttk
greet_ttk = ttk.Label(window, text="No Python")
greet_ttk.pack(pady=5)

# Frame để nhóm các widget còn lại
frame = ttk.Frame(window, padding=(15, 17, 15, 12))
frame.pack(fill="both", expand=True)

# Entry: Nhập 1 dòng
entry_label = ttk.Label(frame, text="Nhập tên của bạn:")
entry_label.pack()
entry = tk.Entry(frame)
entry.pack(pady=5)

# Text: Nhập nhiều dòng
text_label = ttk.Label(frame, text="Ghi chú:")
text_label.pack()
text = tk.Text(frame, height=5)
text.pack(pady=5)

# Button: Khi nhấn sẽ in ra tên nhập vào
def say_hi():
    name = entry.get()
    note = text.get("1.0", tk.END).strip()
    print(f"Xin chào {name}!")
    print(f"Ghi chú của bạn: {note}")

btn = tk.Button(frame, text="Gửi", command=say_hi)
btn.pack(pady=10)

# Chạy vòng lặp chính
window.mainloop()
