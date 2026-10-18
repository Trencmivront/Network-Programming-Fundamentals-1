from tkinter import Button
from logger import get_logger
import logic.WindowHandler as WindowHandler

logger = get_logger("EchoTestButton")


class EchoTestButton(Button):
    def __init__(self, master):
        super().__init__(master, text="Echo Connection Test", width=20)
        self.config(command=self.on_click)

    def on_click(self):
        try:
            from ..panels.EchoPanel import EchoPanel
            root = self.winfo_toplevel()
            WindowHandler.switch_panel(root, EchoPanel)
        except Exception as error:
            logger.error(f"Error opening EchoPanel: {error}", exc_info=True)