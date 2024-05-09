import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import socket

# Hàm lấy dữ liệu từ URL và hiển thị nó trong Listbox
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
url = f'http://{IPAddr}:8000/api/players'
def fetch_data():
    try:
        response = requests.get(url)
        response.raise_for_status()  # Kiểm tra lỗi HTTP

        # Lấy dữ liệu JSON
        data = response.json()

        # Xóa dữ liệu cũ trong Listbox
        listbox.delete(0, tk.END)

        # Thêm dữ liệu mới vào Listbox
        for item in data:
            listbox.insert(tk.END, f"{item['id']}: {item['ingame_name']} - {item['score']}")

    except requests.RequestException as e:
        messagebox.showerror("Lỗi", f"Không thể lấy dữ liệu: {e}")

# Tạo giao diện người dùng với tkinter
root = tk.Tk()
root.title("Lấy Dữ Liệu JSON")

# Tạo nút để lấy dữ liệu
fetch_button = ttk.Button(root, text="Lấy Dữ Liệu", command=fetch_data)
fetch_button.pack(pady=10)

# Tạo Listbox để hiển thị dữ liệu
listbox = tk.Listbox(root, width=50, height=10)
listbox.pack(pady=10)

# Chạy vòng lặp chính của tkinter
root.mainloop()