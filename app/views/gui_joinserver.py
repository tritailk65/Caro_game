from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox, END
import socket
import websocket
import threading
import json

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"E:\Learning\Project_Data\OSSD\design\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

# Get ipv4 local
ws_url = f'ws://{IPAddr}:8000/ws/service-socket/'

class JoinServer:
    def __init__(self):
        window = Tk()

        window.geometry("596x377")
        window.configure(bg = "#FFFFFF")

        #region GUI
        canvas = Canvas(
            window,
            bg = "#FFFFFF",
            height = 377,
            width = 596,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)
        image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        image_1 = canvas.create_image(
            140.0,
            188.0,
            image=image_image_1
        )

        canvas.create_text(
            308.0,
            58.0,
            anchor="nw",
            text="Welcome !",
            fill="#213040",
            font=("DMSans Bold", 32 * -1)
        )

        canvas.create_text(
            308.0,
            132.0,
            anchor="nw",
            text="Enter your name to join server",
            fill="#000000",
            font=("DMSans Regular", 20 * -1)
        )

        entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        entry_bg_1 = canvas.create_image(
            441.0,
            228.5,
            image=entry_image_1
        )
        self.entry_1 = Entry(
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_1.place(
            x=328.0,
            y=206.0,
            width=226.0,
            height=43.0
        )

        button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        button_1 = Button(
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.handle_join(self.entry_1.get()),
            relief="flat"
        )
        button_1.place(
            x=463.0,
            y=292.0,
            width=111.0,
            height=47.0
        )
        window.resizable(False, False)
        window.mainloop()
        #endregion

        self.is_success = False


    def handle_join(self, name):
        self.ws = websocket.WebSocketApp(
            f'ws://{IPAddr}:8000/ws/service-socket/{name}/',
            on_message=handle_message()
        )

        self.ws_thread = threading.Thread(target=self.ws.run_forever)
        self.ws_thread.start()
        self.entry_1.delete(0, END)

        def handle_message(self,message):
            print("Kết nối đã được mở.")
            data = json.loads(message)
            print(data)

