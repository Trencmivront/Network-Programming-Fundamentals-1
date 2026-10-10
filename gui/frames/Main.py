import tkinter as tk
from ..panels.MainButtonSetPanel import MainButtonSetPanel

class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Project - 1")
        self.geometry("800x600")

        mbsp = MainButtonSetPanel(self)
        mbsp.pack(expand=True)
        self.mainloop()
