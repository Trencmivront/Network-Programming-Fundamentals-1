from tkinter import Button

class EchoTestButton(Button):
    def __init__(self, master):
        super().__init__(master, text="Echo Connection Test", width=20)