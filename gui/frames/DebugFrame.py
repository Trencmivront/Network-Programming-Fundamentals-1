import tkinter as tk
from tkinter import Scrollbar, Text

class DebugFrame(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.title("Debug Window")
        self.geometry("700x400")

        # Disable closing the window manually
        self.protocol("WM_DELETE_WINDOW", lambda: None)

        # Scrollable text field that does not accept user input
        scrollbar = Scrollbar(self)
        scrollbar.pack(side="right", fill="y")

        self.text_field = Text(
            self,
            wrap="word",
            state="disabled",
            yscrollcommand=scrollbar.set,
            font=("Arial", 11),
        )
        self.text_field.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.text_field.yview)

    def display_log(self, message: str):
        """Appends a string message to the text field."""
        self.text_field.config(state="normal")
        self.text_field.insert(tk.END, str(message) + "\n")
        self.text_field.see(tk.END)
        self.text_field.config(state="disabled")
    