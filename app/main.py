from tkinter import Tk,Frame
from views.gui_startgame import StartGame
from views.gui_gamemode import GameMode
from views.gui_ranking import Ranking

class windows(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.wm_title("Caro online")
        self.container = Frame(self)
        self.container.pack(side = "top", fill = "both", expand = True) 
        self.current_frame = None

        self.show_frame(StartGame)

    def show_frame(self, cont):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = cont(self.container, controller=self)
        self.current_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    # join = JoinServer()
    # if join.is_success == True:
    #     app = windows()
    #     app.geometry("1300x700")
    #     app.mainloop()

    app = windows()
    app.geometry("1300x700")
    app.resizable(False,False)
    app.mainloop()