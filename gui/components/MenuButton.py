from tkinter import Button

class MenuButton(Button):
    def __init__(self, master, text, width, window):
        self.window = window
        super().__init__(master, text=text, width=width)
        self.config(command=self.on_click)

    def on_click(self):
        try:
            self.window(self).pack()
        except Exception as error:
            print(error)
