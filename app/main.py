from tkinter import Tk,ttk,Frame
from views.gui_startgame import StartGame
from views.gui_gamemode import GameMode
from views.gui_findmatches import FindMatches
from views.gui_ranking import Ranking
from views.gui_gameplay import GamePlay

class windows(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        # Adding a title to the window
        self.wm_title("Caro online")
        # creating a frame and assigning it to container
        container = Frame(self)
        # specifying the region where the frame is packed in root
        container.pack(side = "top", fill = "both", expand = True) 

        # We will now create a dictionary of frames
        self.frames = {}
        # we'll create the frames themselves later but let's add the components to the dictionary.
        for F in (StartGame,GameMode,FindMatches,Ranking,GamePlay):
            frame = F(container, self)
            # the windows class acts as the root window for the frames.
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartGame)

    def show_frame(self, cont):
        frame = self.frames[cont]
        # raises the current frame to the top
        frame.tkraise()

if __name__ == "__main__":
    app = windows()
    app.geometry("1300x700")
    app.mainloop()