from tkinter import Button

class RetrieveTimeButton(Button):
    def __init__(self, master):
        super().__init__(master, text="Retrieve Current Time", width=20)