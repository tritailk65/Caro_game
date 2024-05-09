import tkinter as tk
import threading
import time

# Frame đại diện cho màn hình game board
class GameBoard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # Giả định rằng việc khởi tạo mất một thời gian dài (ví dụ: tải dữ liệu)
        self.label = tk.Label(self, text="Game board loading...")
        self.label.pack()

    def initialize(self):
        # Thực hiện các tác vụ khởi tạo tốn thời gian
        time.sleep(5)  # Giả lập quá trình khởi tạo dài
        self.label.config(text="Game board loaded!")
        # Sau khi khởi tạo xong, chuyển về frame game board
        self.controller.show_frame("GameBoard")

# Frame đại diện cho màn hình loading
class Loading(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Loading...").pack()

# Lớp ứng dụng chính chứa các frame
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My Application")

        # Container frame để chứa các frame con
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        # Sử dụng một từ điển để quản lý các frame con
        self.frames = {}

        # Tạo các frame con và thêm vào container
        for F in (Loading, GameBoard):
            frame = F(container, self)  # Tạo frame với controller là 'self'
            self.frames[F.__name__] = frame  # Sử dụng tên của lớp để làm key trong từ điển
            frame.grid(row=0, column=0, sticky="nsew")  # Đặt frame trong container

        self.show_frame("Loading")  # Hiển thị frame loading trước

        # Chạy việc khởi tạo trong một luồng riêng biệt
        threading.Thread(target=self.initialize_gameboard).start()

    # Phương thức chuyển đổi giữa các frame
    def show_frame(self, page_name):
        frame = self.frames[page_name]  # Tìm frame theo tên
        frame.tkraise()  # Đưa frame lên phía trước

    def initialize_gameboard(self):
        # Khởi tạo gameboard trong một luồng riêng
        gameboard = self.frames["GameBoard"]
        gameboard.initialize()  # Khởi tạo game board
        # Khi hoàn thành, chuyển về frame game board
        self.show_frame("GameBoard")

# Chạy ứng dụng
if __name__ == "__main__":
    app = App()
    app.mainloop()
