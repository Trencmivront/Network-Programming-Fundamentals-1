from tkinter import Button
from logger import get_logger
import logic.WindowHandler as WindowHandler

logger = get_logger("ChatButton")


class ChatButton(Button):
    def __init__(self, master):
        super().__init__(master, text="Chat", width=20)
        self.config(command=self.on_click)

    def on_click(self):
        try:
            from ..panels.ChatPanel import ChatPanel
            root = self.winfo_toplevel()
            WindowHandler.switch_panel(root, ChatPanel)
        except Exception as error:
            logger.error(f"Error opening ChatPanel: {error}", exc_info=True)