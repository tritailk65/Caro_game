from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame, messagebox, END
import views.gui_gamemode

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
        canvas = Canvas(
            self,
            bg = "#FFFFFF",
            height = 700,
            width = 1300,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)
        canvas.create_rectangle(
            0.0,
            114.0,
            1300.0,
            596.0,
            fill="#101B27",
            outline="")

        canvas.create_rectangle(
            0.0,
            596.0,
            1300.0,
            700.0,
            fill="#1B2837",
            outline="")

        canvas.create_rectangle(
            0.0,
            0.0,
            1300.0,
            114.0,
            fill="#1B2837",
            outline="")

        canvas.create_rectangle(
            179.0,
            54.0,
            194.0,
            69.0,
            fill="#FF0000",
            outline="")

        self.image_image_1 = PhotoImage(
            file=relative_to_assets("avatar_player1.png"))
        canvas.create_image(
            571.0,
            59.0,
            image=self.image_image_1
        )

        self.image_image_2 = PhotoImage(
            file=relative_to_assets("avatar_player2.png"))
        canvas.create_image(
            727.0,
            59.0,
            image=self.image_image_2
        )

        canvas.create_text(
            625.0,
            51.0,
            anchor="nw",
            text="0",
            fill="#FFFFFF",
            font=("Inter SemiBold", 20 * -1)
        )

        canvas.create_text(
            661.0,
            51.0,
            anchor="nw",
            text="0",
            fill="#FFFFFF",
            font=("Inter SemiBold", 20 * -1)
        )

        canvas.create_text(
            477.0,
            70.0,
            anchor="nw",
            text="5:00",
            fill="#FF00D6",
            font=("Inter SemiBold", 16 * -1)
        )

        canvas.create_text(
            778.0,
            70.0,
            anchor="nw",
            text="5:00",
            fill="#FFE500",
            font=("Inter SemiBold", 16 * -1)
        )

        canvas.create_text(
            440.0,
            42.0,
            anchor="nw",
            text="Player 1",
            fill="#FFFFFF",
            font=("Inter Bold", 20 * -1)
        )

        canvas.create_text(
            777.0,
            42.0,
            anchor="nw",
            text="Player 2",
            fill="#FFFFFF",
            font=("Inter Bold", 20 * -1)
        )

        canvas.create_rectangle(
            1104.0,
            53.0,
            1119.0,
            68.0,
            fill="#00FF00",
            outline="")

        canvas.create_rectangle(
            1154.0,
            37.0,
            1183.0,
            85.0,
            fill="#FF0000",
            outline="")

        canvas.create_text(
            1161.0,
            47.0,
            anchor="nw",
            text="7",
            fill="#FFFFFF",
            font=("Inter Bold", 24 * -1)
        )

        canvas.create_rectangle(
            118.0,
            34.0,
            147.0,
            82.0,
            fill="#FF0000",
            outline="")

        canvas.create_text(
            125.0,
            44.0,
            anchor="nw",
            text="7",
            fill="#FFFFFF",
            font=("Inter Bold", 24 * -1)
        )
        #endregion

        GameBoard(self)

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

        def handle_cancle_match():
            result = messagebox.askquestion("Hủy trận đấu","Bạn có chắc chắn muốn hủy trận đấu ?")

            if result == 'yes':
                controller.show_frame(views.gui_gamemode.GameMode)

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
