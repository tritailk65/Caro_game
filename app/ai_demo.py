import tkinter as tk
import random
from tkinter import messagebox

# Xác định biểu tượng cho người chơi và máy tính
PLAYER_X = 'X'
PLAYER_O = 'O'

# Kiểm tra xem có ai thắng trò chơi hay không
def check_win(board, player):
    # Kiểm tra hàng ngang
    for row in board:
        if all([s == player for s in row]):
            return True
    # Kiểm tra hàng dọc
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    # Kiểm tra đường chéo
    if all([board[i][i] == player for i in range(3)]):
        return True
    if all([board[i][2-i] == player for i in range(3)]):
        return True
    return False

# Kiểm tra xem trò chơi có hoà hay không
def check_draw(board):
    return all([board[row][col] != '' for row in range(3) for col in range(3)])

# Thuật toán Minimax để máy tính chọn bước đi tốt nhất
def minimax(board, is_maximizing):
    if check_win(board, PLAYER_X):
        return -1  # Người chơi thắng
    if check_win(board, PLAYER_O):
        return 1  # Máy tính thắng
    if check_draw(board):
        return 0  # Hoà

    if is_maximizing:
        best_score = -float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == '':
                    board[row][col] = PLAYER_O
                    score = minimax(board, False)
                    board[row][col] = ''
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == '':
                    board[row][col] = PLAYER_X
                    score = minimax(board, True)
                    board[row][col] = ''
                    best_score = min(best_score, score)
        return best_score

# Máy tính chọn bước đi dựa trên Minimax
def computer_move(board):
    best_score = -float('inf')
    best_move = None
    for row in range(3):
        for col in range(3):
            if board[row][col] == '':
                board[row][col] = PLAYER_O
                score = minimax(board, False)
                board[row][col] = ''
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    return best_move

# Lớp TicTacToe với Tkinter
class TicTacToe(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic Tac Toe with Minimax")
        self.geometry("300x300")
        self.reset_game()
        self.create_widgets()

    def reset_game(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = PLAYER_X  # Bắt đầu với người chơi
        self.game_over = False

    def create_widgets(self):
        self.buttons = []
        for row in range(3):
            button_row = []
            for col in range(3):
                button = tk.Button(
                    self,
                    text='',
                    font=('Arial', 40),
                    width=3,
                    height=1,
                    command=lambda r=row, c=col: self.player_move(r, c)
                )
                button.grid(row=row, column=col)
                button_row.append(button)
            self.buttons.append(button_row)

    def player_move(self, row, col):
        if self.game_over or self.board[row][col] != '':
            return
        self.board[row][col] = self.current_player
        self.buttons[row][col].configure(text=self.current_player)

        if check_win(self.board, self.current_player):
            self.game_over = True
            messagebox.showinfo("Game Over", f"{self.current_player} wins!")
            return

        if check_draw(self.board):
            self.game_over = True
            messagebox.showinfo("Game Over", "It's a draw!")
            return

        self.current_player = PLAYER_O  # Chuyển sang máy tính

        # Máy tính thực hiện bước đi
        move = computer_move(self.board)
        if move:
            row, col = move
            self.board[row][col] = self.current_player
            self.buttons[row][col].configure(text=self.current_player)

            if check_win(self.board, self.current_player):
                self.game_over = True
                messagebox.showinfo("Game Over", f"{self.current_player} wins!")
                return

            if check_draw(self.board):
                self.game_over = True
                messagebox.showinfo("Game Over", "It's a draw!")
                return

        self.current_player = PLAYER_X  # Quay lại người chơi

# Khởi chạy trò chơi
if __name__ == "__main__":
    game = TicTacToe()
    game.mainloop()
