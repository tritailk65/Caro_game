import tkinter as tk
from tkinter import messagebox
import threading
import websocket
import json

def on_message(ws, message):
    # Chuyển đổi tin nhắn thành định dạng JSON
    data = json.loads(message)
    return data

class TicTacToe:
    def __init__(self, root,ws_url,player_symbol):
        self.root = root
        self.root.title("Tic Tac Toe")

        self.ws = websocket.WebSocketApp(
            ws_url,
            on_message=self.handle_message
        )

        # Tạo luồng để chạy WebSocket
        self.ws_thread = threading.Thread(target=self.ws.run_forever)
        self.ws_thread.start()

        # Tạo bảng 3x3
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.current_player = player_symbol

        self.create_board()

    def handle_message(self,ws,message):
        # Chuyển đổi tin nhắn từ WebSocket thành định dạng JSON
        data = json.loads(message)

        if data.get("type") == "connect_established":
            self.root.after(0, lambda: messagebox.showinfo("Server Message", f"Message from server: {data["message"]}"))

        # Chuyển đổi tin nhắn từ WebSocket thành định dạng JSON
        if data.get("type") == "move":
            row = data["position"]["row"]
            col = data["position"]["column"]
            player = data["player"]

            # Sử dụng self.root.after để cập nhật GUI trong luồng chính
            self.root.after(0, lambda: self.update_board(row, col, player))
        else:
            # Xử lý các loại tin nhắn khác
            pass

    def create_board(self):
        for row in range(3):
            for col in range(3):
                button = tk.Button(
                    self.root,
                    text=' ',
                    width=10,
                    height=3,
                    font=("Arial", 18, "bold"),
                    command=lambda r=row, c=col: self.make_move(r, c)
                )
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)

            move_data = {
                "type": "move",
                "player": self.current_player,
                "position": {
                    "row": row,
                    "column": col
                }
            }
            self.ws.send(json.dumps(move_data))

            if self.check_winner(self.current_player):
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_game()
            elif self.is_full():
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_game()
        else:
            messagebox.showwarning("Invalid Move", "Please select an empty spot.")

    def check_winner(self, player):
        # Kiểm tra hàng
        for row in self.board:
            if all(spot == player for spot in row):
                return True
        # Kiểm tra cột
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        # Kiểm tra chéo
        if all(self.board[i][i] == player for i in range(3)):
            return True
        if all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def is_full(self):
        # Kiểm tra xem bảng đã đầy chưa
        return all(self.board[row][col] != ' ' for row in range(3) for col in range(3))

    def reset_game(self):
        # Reset bảng
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        for row in range(3):
            for col in range(3):
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

if __name__ == "__main__":
    root = tk.Tk()
    player_symbol = "O"
    ws_url = "ws://192.168.210.201:8000/ws/socket-server/"
    game = TicTacToe(root,ws_url,player_symbol)
    root.mainloop()