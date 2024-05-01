import tkinter as tk
from tkinter import messagebox, Frame, Button,Entry,END
import threading
import websocket
import json
from enum import Enum
from views.gui_chat import FrameChat

ROW = 16
COL = 18

class GameMode(Enum):
    ONLINE = 1
    FRIEND = 2
    AI = 3

def on_message(ws, message):
    # Chuyển đổi tin nhắn thành định dạng JSON
    data = json.loads(message)
    return data

ws_url = "ws://192.168.210.201:8000/ws/socket-server/"

class GameBoard:
    def __init__(self,root,mode):
        self.root = root
        self.mode = GameMode(mode).name

        self.frame = Frame(self.root, bg="#FFFFFF", width=540, height=480)
        self.frame.place(x=380, y=115)

        self.entryMsg = Entry(root,
                              bg="#2C3E50",
                              fg="#EAECEE",
                              font="Helvetica 13")
        self.buttonMsg = Button(root,
                                text="Send",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#ABB2B9",
                                command=lambda: self.send_message(self.entryMsg.get()))

        if self.mode == "ONLINE":
            # Thêm khung chat
            self.chat = FrameChat(self.root)

            self.ws = websocket.WebSocketApp(
                ws_url,
                on_message=self.handle_message
            )

            # Tạo luồng để chạy WebSocket
            self.ws_thread = threading.Thread(target=self.ws.run_forever)
            self.ws_thread.start()
        
            self.entryMsg.place(x=584,y=630,width=611,height=36)
    
            self.buttonMsg.place(x=1200,y=630,width=60,height=36)
 
        self.entryMsg.focus()

        self.board = [[' ' for _ in range(COL)] for _ in range(ROW)]
        self.buttons = [[None for _ in range(COL)] for _ in range(ROW)]
        
        # Tạo lưới Square với 16 hàng và 18 cột
        self.create_grid(ROW, COL)

        self.current_player = "X"

    def create_grid(self, rows, cols):
        for row in range(rows):
            for col in range(cols):
                # Tạo nút với tọa độ theo hàng và cột
                self.buttons[row][col] = Button(
                    self.frame, 
                    text=' ',
                    bg="#ffffff", 
                    bd=1, 
                    relief='solid',
                    font=("Arial", 18, "bold"),
                    command=lambda r=row, c=col: self.make_move(r, c)
                )
                self.buttons[row][col].place(x=col*30, y=row * 30,width=30, height=30)

    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)

            if self.mode == "ONLINE":
                move_data = {
                    "type": "move",
                    "player": self.current_player,
                    "position": {
                        "row": row,
                        "col": col
                    }
                }
                self.ws.send(json.dumps(move_data))

            if self.mode == "FRIEND":
                if self.check_winner(self.current_player):
                    messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                    self.reset_game()
                elif self.is_full():
                    messagebox.showinfo("Game Over", "It's a tie!")
                    self.reset_game()
                else:
                    self.current_player = 'X' if self.current_player == 'O' else 'O'

    def check_winner(self, player):
        # Số quân cờ cần thiết để chiến thắng
        winning_count = 5
        
        # Kiểm tra các hàng
        for row in range(ROW):
            for col in range(COL - winning_count + 1):
                if all(self.board[row][c] == player for c in range(col, col + winning_count)):
                    return True
        
        # Kiểm tra các cột
        for col in range(COL):
            for row in range(ROW - winning_count + 1):
                if all(self.board[r][col] == player for r in range(row, row + winning_count)):
                    return True
        
        # Kiểm tra các đường chéo chính (từ trên trái đến dưới phải)
        for row in range(ROW - winning_count + 1):
            for col in range(COL - winning_count + 1):
                if all(self.board[row + i][col + i] == player for i in range(winning_count)):
                    return True
        
        # Kiểm tra các đường chéo phụ (từ trên phải đến dưới trái)
        for row in range(ROW - winning_count + 1):
            for col in range(winning_count - 1, COL):
                if all(self.board[row + i][col - i] == player for i in range(winning_count)):
                    return True

        return False

    def is_full(self):
        # Kiểm tra xem bảng đã đầy chưa
        return all(self.board[row][col] != ' ' for row in range(ROW) for col in range(COL))

    def reset_game(self):
        # Reset bảng
        self.board = [[' ' for _ in range(COL)] for _ in range(ROW)]
        for row in range(ROW):
            for col in range(COL):
                self.buttons[row][col].config(text=' ')

    def update_board(self, row, col, player):
        # Cập nhật giao diện bảng trò chơi
        if self.board[row][col] == ' ':
            self.board[row][col] = player
            self.buttons[row][col].config(text=player)

            if self.check_winner(player):
                messagebox.showinfo("Game Over", f"Player {player} wins!")
                self.reset_game()
            elif self.is_full():
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_game()

    def handle_message(self,ws,message):
        # Chuyển đổi tin nhắn từ WebSocket thành định dạng JSON
        data = json.loads(message)

        if data.get("type") == "Matching":
            self.root.after(0, lambda: messagebox.showinfo("Server Message", f"Message from server: {data["message"]}"))
            self.current_player = data["symbol"]

        # Chuyển đổi tin nhắn từ WebSocket thành định dạng JSON
        if data.get("type") == "move":
            row = data["position"]["row"]
            col = data["position"]["col"]
            player = data["player"]

            # Sử dụng self.root.after để cập nhật GUI trong luồng chính
            self.root.after(0, lambda: self.update_board(row, col, player))

        if data.get("type") == "chat":
            self.chat.insert_text("Player " + self.current_player +": " + data["message"] + "\n\n")

        else:
            # Xử lý các loại tin nhắn khác
            pass

    def send_message(self,message):
        chat_data = {
            "type": "chat",
            "message": message
        }
        self.entryMsg.delete(0, END)
        self.ws.send(json.dumps(chat_data))