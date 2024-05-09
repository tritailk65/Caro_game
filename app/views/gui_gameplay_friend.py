from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame, messagebox, END
import views.gui_gamemode
import time
from views.gui_loadingUI import Loading
import threading

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"..\assets")

ROW = 16
COL = 18

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class GamePlayWithFriend(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self, parent)

        #region GUI Gameplay
        self.canvas = Canvas(
            self,
            bg = "#FFFFFF",
            height = 700,
            width = 1300,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.canvas.create_rectangle(
            0.0,
            114.0,
            1300.0,
            596.0,
            fill="#101B27",
            outline="")

        self.canvas.create_rectangle(
            0.0,
            596.0,
            1300.0,
            700.0,
            fill="#1B2837",
            outline="")

        self.canvas.create_rectangle(
            0.0,
            0.0,
            1300.0,
            114.0,
            fill="#1B2837",
            outline="")

        self.image_image_1 = PhotoImage(
            file=relative_to_assets("oggy.png"))
        self.canvas.create_image(
            571.0,
            59.0,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=relative_to_assets("jack.png"))
        self.canvas.create_image(
            727.0,
            59.0,
            image=self.image_image_2
        )

        self.SCORE_X = 0
        self.SCORE_O = 0

        # Score player 1
        self.score_player1 = self.canvas.create_text(
            625.0,
            51.0,
            anchor="nw",
            text=self.SCORE_X,
            fill="#FFFFFF",
            font=("Inter SemiBold", 20 * -1)
        )

        # Score player 2
        self.score_player2 = self.canvas.create_text(
            661.0,
            51.0,
            anchor="nw",
            text=self.SCORE_O,
            fill="#FFFFFF",
            font=("Inter SemiBold", 20 * -1)
        )

        self.canvas.create_text(
            440.0,
            42.0,
            anchor="nw",
            text="Oggy",
            fill="#FFFFFF",
            font=("Inter Bold", 20 * -1)
        )

        self.canvas.create_text(
            777.0,
            42.0,
            anchor="nw",
            text="Jack",
            fill="#FFFFFF",
            font=("Inter Bold", 20 * -1)
        )

        #endregion
        self.controller = controller

        # Cancle match btn
        self.button_image_1 = PhotoImage(
            file=relative_to_assets("cancle_match_btn.png"))
        button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: handle_cancle_match(),
            relief="flat"
        )
        button_1.place(
            x=35.0,
            y=618.0,
            width=200.375,
            height=58.0
        )
        threading.Thread(target=self.loading_board).start()

        def handle_cancle_match():
            result = messagebox.askquestion("Hủy trận đấu","Bạn có chắc chắn muốn hủy trận đấu ?")

            if result == 'yes':
                controller.show_frame(views.gui_gamemode.GameMode)

    def loading_board(self):
        self.game = GameBoard(self)
        

class GameBoard:
    def __init__(self,root):
        self.root = root

        self.frame = Frame(self.root, bg="#FFFFFF", width=540, height=480)
        self.frame.place(x=380, y=115)

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
                    if self.current_player == "X":
                        self.root.SCORE_X += 1
                        self.root.canvas.itemconfig(self.root.score_player1,text=self.root.SCORE_X)
                    if self.current_player == "O":
                        self.root.SCORE_O += 1
                        self.root.canvas.itemconfig(self.root.score_player2,text=self.root.SCORE_O)
                    return True
        
        # Kiểm tra các cột
        for col in range(COL):
            for row in range(ROW - winning_count + 1):
                if all(self.board[r][col] == player for r in range(row, row + winning_count)):
                    if self.current_player == "X":
                        self.root.SCORE_X += 1
                        self.root.canvas.itemconfig(self.root.score_player1,text=self.root.SCORE_X)
                    if self.current_player == "O":
                        self.root.SCORE_O += 1
                        self.root.canvas.itemconfig(self.root.score_player2,text=self.root.SCORE_O)
                    return True
        
        # Kiểm tra các đường chéo chính (từ trên trái đến dưới phải)
        for row in range(ROW - winning_count + 1):
            for col in range(COL - winning_count + 1):
                if all(self.board[row + i][col + i] == player for i in range(winning_count)):
                    if self.current_player == "X":
                        self.root.SCORE_X += 1
                        self.root.canvas.itemconfig(self.root.score_player1,text=self.root.SCORE_X)
                    if self.current_player == "O":
                        self.root.SCORE_O += 1
                        self.root.canvas.itemconfig(self.root.score_player2,text=self.root.SCORE_O)
                    return True
        
        # Kiểm tra các đường chéo phụ (từ trên phải đến dưới trái)
        for row in range(ROW - winning_count + 1):
            for col in range(winning_count - 1, COL):
                if all(self.board[row + i][col - i] == player for i in range(winning_count)):
                    if self.current_player == "X":
                        self.root.SCORE_X += 1
                        self.root.canvas.itemconfig(self.root.score_player1,text=self.root.SCORE_X)
                    if self.current_player == "O":
                        self.root.SCORE_O += 1
                        self.root.canvas.itemconfig(self.root.score_player2,text=self.root.SCORE_O)
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
