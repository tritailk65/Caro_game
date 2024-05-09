from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame, messagebox, END
import views.gui_gamemode
import time
from views.gui_loadingUI import Loading
import threading

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"..\assets")

ROW = 16
COL = 16
SIZE = 16
WIN_SCORE = 100_000_000
DEPTH = 3

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class GamePlayAI(Frame):
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

        # canvas.create_rectangle(
        #     179.0,
        #     54.0,
        #     194.0,
        #     69.0,
        #     fill="#FF0000",
        #     outline="")

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

        # canvas.create_text(
        #     477.0,
        #     70.0,
        #     anchor="nw",
        #     text="5:00",
        #     fill="#FF00D6",
        #     font=("Inter SemiBold", 16 * -1)
        # )

        # canvas.create_text(
        #     778.0,
        #     70.0,
        #     anchor="nw",
        #     text="5:00",
        #     fill="#FFE500",
        #     font=("Inter SemiBold", 16 * -1)
        # )

        self.canvas.create_text(
            470.0,
            42.0,
            anchor="nw",
            text="You",
            fill="#FFFFFF",
            font=("Inter Bold", 20 * -1)
        )

        self.canvas.create_text(
            800.0,
            42.0,
            anchor="nw",
            text="Bot",
            fill="#FFFFFF",
            font=("Inter Bold", 20 * -1)
        )

        # canvas.create_rectangle(
        #     1104.0,
        #     53.0,
        #     1119.0,
        #     68.0,
        #     fill="#00FF00",
        #     outline="")

        # canvas.create_rectangle(
        #     1154.0,
        #     37.0,
        #     1183.0,
        #     85.0,
        #     fill="#FF0000",
        #     outline="")

        # canvas.create_text(
        #     1161.0,
        #     47.0,
        #     anchor="nw",
        #     text="7",
        #     fill="#FFFFFF",
        #     font=("Inter Bold", 24 * -1)
        # )

        # canvas.create_rectangle(
        #     118.0,
        #     34.0,
        #     147.0,
        #     82.0,
        #     fill="#FF0000",
        #     outline="")

        # canvas.create_text(
        #     125.0,
        #     44.0,
        #     anchor="nw",
        #     text="7",
        #     fill="#FFFFFF",
        #     font=("Inter Bold", 24 * -1)
        # )
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

        self.frame = Frame(self.root, bg="#FFFFFF", width=480, height=480)
        self.frame.place(x=410, y=114)

        self.board = [[' ' for _ in range(COL)] for _ in range(ROW)]
        self.buttons = [[None for _ in range(COL)] for _ in range(ROW)]
        
        # Tạo lưới Square với 16 hàng và 18 cột
        self.create_grid(ROW, COL)

        self.current_player = "X"

        self.evaluationCount = 0

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
                    command=lambda r=row, c=col: self.player_make_move(r, c)
                )
                self.buttons[row][col].place(x=col*30, y=row * 30,width=30, height=30)

    def player_make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)

            if self.check_winner == 2:
                messagebox.showinfo("Game over", f"You wins!")
                self.reset_game()
            
            move = self.caculate_next_move()
            if move != None:
                self.make_move(move[0],move[1],self.board, self.buttons)

            if self.check_winner == 1:
                messagebox.showinfo("Game over", f"AI wins!")
                self.reset_game()

    def make_move(self, row, col, board,buttons):
        board[row][col] = 'O'
        if buttons != None:
            buttons[row][col].config(text='O')

    def check_winner(self):
        if self.get_score(self.board, True,False) >= WIN_SCORE: return 2
        if self.get_score(self.board, False, True) >= WIN_SCORE: return 1
        return 0

    def is_full(self):
        # Kiểm tra xem bảng đã đầy chưa
        return all(self.board[row][col] != ' ' for row in range(ROW) for col in range(COL))

    def reset_game(self):
        # Reset bảng
        self.board = [[' ' for _ in range(COL)] for _ in range(ROW)]
        for row in range(ROW):
            for col in range(COL):
                self.buttons[row][col].config(text=' ')

    # Tìm các nước đi có thể
    def generate_move(self, dummyBoard):
        move_list = []
        for row in range(SIZE):
            for col in range(SIZE):
                if dummyBoard[row][col] != " ":
                    continue
                if row > 0:
                    if col > 0: 
                        if dummyBoard[row-1][col-1] != " " or dummyBoard[row][col-1] != " ": 
                            move_list.append([row, col])
                            continue
                    if col < SIZE-1:
                        if dummyBoard[row-1][col+1] != " " or dummyBoard[row][col+1] != " ":
                            move_list.append([row, col])
                            continue
                    if dummyBoard[row-1][col] != " " :
                        move_list.append([row, col])
                        continue
                if row < SIZE-1:
                    if col > 0:
                        if dummyBoard[row+1][col-1] != " " or dummyBoard[row][col-1] != " ":
                            move_list.append([row, col])
                            continue
                    if col < SIZE-1: 
                        if dummyBoard[row+1][col+1] != " " or dummyBoard[row][col+1] != " ":
                            move_list.append([row, col])
                            continue
                    if dummyBoard[row+1][col] != " ":
                        move_list.append([row, col])
                        continue
        return move_list

    def remove_move(self, board, x, y):
        board[x][y] = ' '

    def caculate_next_move(self):
        best_move = self.search_winning_move(self.board)
        move = [None] * 2
        if best_move != None:
            move[0] = best_move[1]
            move[1] = best_move[2]
        else:
            dummyBoard = [[' ' for _ in range(SIZE)] for _ in range(SIZE)]
            for i in range(SIZE):
                for j in range(SIZE):
                    dummyBoard[i][j] = self.board[i][j]
            best_move = self.minimaxSearchAB(DEPTH, dummyBoard, True, -1.0, WIN_SCORE)
            if best_move[1] == None:
                move = None
            else:
                move[0] = best_move[1]
                move[1] = best_move[2]
        self.evaluationCount = 0
        return move

    def minimaxSearchAB(self, depth, dummyBoard, max, alpha, beta):
        if depth == 0:
            x = [self.evaluateBoardForWhite(dummyBoard, not max), None, None]
            return x
        allPossibleMoves = self.generate_move(dummyBoard)
        if len(allPossibleMoves) == 0:
            x = [self.evaluateBoardForWhite(dummyBoard, not max), None, None]
            return x
        bestMove = [None] * 3
        if max: 
            bestMove[0] = -1.0
            for move in allPossibleMoves:
                self.make_move(move[1], move[0],dummyBoard, None)
                tempMove = self.minimaxSearchAB(depth-1, dummyBoard, False, alpha, beta)
                self.remove_move(dummyBoard,move[1], move[0])
                if tempMove[0] > alpha: alpha = tempMove[0]
                if tempMove[0] >= beta: return tempMove
                if tempMove[0] > bestMove[0]:
                    bestMove = tempMove
                    bestMove[1] = move[0]
                    bestMove[2] = move[1]
        else:
            bestMove[0] = 100_000_000.0
            bestMove[1] = allPossibleMoves[0][0]
            bestMove[2] = allPossibleMoves[0][1]
            for move in allPossibleMoves:
                self.make_move(move[1],move[0],dummyBoard, None)
                tempMove = self.minimaxSearchAB(depth-1, dummyBoard, True, alpha, beta)
                self.remove_move( dummyBoard,move[1],move[0])
                if tempMove[0] < beta: beta = tempMove[0]
                if tempMove[0] <= alpha: return tempMove
                if tempMove[0] < bestMove[0]:
                    bestMove = tempMove
                    bestMove[1] = move[0]
                    bestMove[2] = move[1]
        return bestMove

    def search_winning_move(self, board):
        allPossibleMoves = self.generate_move(board)
        winning_move = [None] * 3
        for move in allPossibleMoves:
            self.evaluationCount+=1
            dummyBoard = [[' ' for _ in range(SIZE)] for _ in range(SIZE)]
            for i in range(SIZE):
                for j in range(SIZE):
                    dummyBoard[i][j] = board[i][j]
            self.make_move(move[1],move[0],dummyBoard,None)
            if self.get_score(dummyBoard,False,False) >= WIN_SCORE:
                winning_move[1] = move[0]
                winning_move[2] = move[1]
                return winning_move
        return None

    def get_score(self,dummyBoard, forBlack, blacksTurn):
        matrixBoard = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
        for i in range(SIZE):
            for j in range(SIZE):
                if dummyBoard[i][j] == ' ': matrixBoard[i][j] = 0
                if dummyBoard[i][j] == 'X': matrixBoard[i][j] = 2
                if dummyBoard[i][j] == 'O': matrixBoard[i][j] = 1
        return self.evaluateHorizontal(matrixBoard, forBlack, blacksTurn) + self.evaluateVertical(matrixBoard, forBlack, blacksTurn) + self.evaluateDiagonal(matrixBoard, forBlack, blacksTurn)

    def evaluateHorizontal(self, boardMatrix, forBlack, playersTurn):
        evaluations = [0, 2, 0]
        for i in range(0,len(boardMatrix)):
            for j in range(0,len(boardMatrix[0])):
                self.evaluateDirections(boardMatrix, i, j, forBlack, playersTurn, evaluations)
            self.evaluateDirectionsAfterOnePass(evaluations, forBlack, playersTurn)
        return evaluations[2]

    def evaluateVertical(self, boardMatrix, forBlack, playersTurn):
        evaluations = [0, 2, 0]
        for j in range(0,len(boardMatrix[0])):
            for i in range(0,len(boardMatrix)):
                self.evaluateDirections(boardMatrix, i, j, forBlack, playersTurn, evaluations)
            self.evaluateDirectionsAfterOnePass(evaluations,playersTurn,evaluations)
        return evaluations[2]

    def evaluateDiagonal(self, boardMatrix, forBlack, playersTurn):
        evaluations = [0, 2, 0]
        for k in range(2*(len(boardMatrix)-1)+1):
            isStart = max(0, k - len(boardMatrix) + 1)
            isEnd = min(len(boardMatrix) - 1, k)
            for i in range(isStart,isEnd + 1):
                self.evaluateDirections(boardMatrix, i, k-i, forBlack, playersTurn, evaluations)
            self.evaluateDirectionsAfterOnePass(evaluations, forBlack, playersTurn)
        for k in range(1-len(boardMatrix),len(boardMatrix)):
            iStart = max(0, k)
            iEnd = min(len(boardMatrix) + k - 1, len(boardMatrix) - 1)
            for i in range(iStart, iEnd+1):
                self.evaluateDirections(boardMatrix,i,i-k,forBlack,playersTurn,evaluations)
            self.evaluateDirectionsAfterOnePass(evaluations,forBlack,playersTurn)
        return evaluations[2]

    def evaluateDirections(self, boardMatrix, i, j, isBot, botsTurn, eval):
        if boardMatrix[i][j] == (2 if isBot else 1):
            eval[0]+=1
        elif boardMatrix[i][j] == 0:
            if eval[0] > 0:
                eval[1]-=1
                eval[2] += self.getConsecutiveSetScore(eval[0], eval[1], isBot == botsTurn)
                eval[0] = 0
            eval[1] = 1
        else:
            if eval[0] > 0:
                eval[2] += self.getConsecutiveSetScore(eval[0], eval[1], isBot == botsTurn)
                eval[0] = 0
                eval[1] = 2
            eval[1] = 2

    def evaluateDirectionsAfterOnePass(self, eval, isBot, playersTurn):
        if eval[0] > 0:
            eval[2] += self.getConsecutiveSetScore(eval[0],eval[1], isBot == playersTurn)
        else:
            eval[0] = 0
            eval[1] = 2

    def getConsecutiveSetScore(self,count,blocks, currentTurn):
        winGuarantee = 1000000
        if blocks == 2 and count < 5: return 0
        if count == 5: return WIN_SCORE
        if count == 4:
            if currentTurn: return winGuarantee
            else:
                if blocks == 0: return winGuarantee/4
                else: return 200
        if count == 3:
            if blocks == 0:
                if currentTurn: return 50_000
                else: return 200
            else:
                if currentTurn: return 10
                else: return 5
        if count == 2:
            if blocks == 0:
                if currentTurn: return 7
                else: return 5
            else: return 3
        if count == 1:
            return 1
        return WIN_SCORE*2

    def evaluateBoardForWhite(self, board, blacksTurn):
        self.evaluationCount+=1
        blackScore = self.get_score(board, True, blacksTurn)
        whiteScore = self.get_score(board, False, blacksTurn)
        if blackScore == 0:
            blackScore = 1.0
        return whiteScore/blackScore
