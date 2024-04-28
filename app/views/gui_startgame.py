from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,ttk,Frame
from tkinter import ttk
from views.gui_gamemode import GameMode
import time

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"..\assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class StartGame(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self, parent)

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
        self.image_image_1 = PhotoImage(file=relative_to_assets("start_game.png"))
        canvas.create_image(
            650.0,
            350.0,
            image=self.image_image_1
        )

        # Chỉnh style progressbar
        style = ttk.Style(self)
        style.theme_use('default') 
        style.configure('Custom.Horizontal.TProgressbar', 
                        troughcolor='#385682',
                        background='#5297FF',
                        thickness=20) 
        
        # Tạo thanh tiến trình
        progress_bar = ttk.Progressbar(self, orient='horizontal', mode='determinate', length=1000, style='Custom.Horizontal.TProgressbar')
        progress_bar.grid(column=0, row=0, padx=150, pady=549)

        percent_label = canvas.create_text(
            561.0,
            596.0,
            anchor="nw",
            text="0% completed",
            fill="#C6DDFF",
            font=("DMSans Medium", 24 * -1)
        )

        # Hàm cập nhật tiến trình, load data
        def start_progress(self,progress_bar, canvas, percent_label):
            progress_bar['value'] = 0
            max_steps = 100

            for i in range(1, max_steps + 1):
                time.sleep(0.05) # mô phỏng
                progress_bar['value'] = i  
                # Tính phần trăm hoàn thành
                percentage = int((i / max_steps) * 100)
                # Cập nhật văn bản trên canvas
                canvas.itemconfig(percent_label, text=f"{percentage}% completed")
                self.update_idletasks() 

            time.sleep(0.05)
            controller.show_frame(GameMode)


        # Bắt đầu tiến trình sau 2s start game
        self.after(2000, lambda: start_progress(self, progress_bar, canvas, percent_label))