from tkinter import Frame, Text, Scrollbar,END,DISABLED,NORMAL,Entry,Button,Label

class FrameChat:
    def __init__(self,root):
        self.root = root

        self.frame = Frame(self.root, bg="#101B27", width=315, height=451,                                
                                bd=2, 
                                relief='solid')
        self.frame.place(x=971, y=129)

        self.textCons = Text(self.frame,
                                bg="#101B27",
                                fg="#EAECEE",
                                font="Helvetica 12")
        self.textCons.place(x=10,y=10,width=295,height=431)
 
        self.textCons.config(cursor="arrow")
 
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)

        scrollbar.place(relheight=1,
                        relx=0.94)
 
        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)
    
    def insert_text(self,message):
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END,message)
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

