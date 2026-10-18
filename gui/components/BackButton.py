from tkinter import Button
from logger import get_logger
import logic.WindowHandler as WindowHandler

logger = get_logger("BackButton")

class BackButton(Button):
    """Button to return from any panel back to the previous panel."""
    def __init__(self, master, text="Back", width=15):
        super().__init__(master, text=text, width=width)
        self.config(command=self.on_click)

    def on_click(self):
        try:
            root = self.winfo_toplevel()
            # Pass root explicitly into WindowHandler so the logic
            # is fully decoupled from the Main class.
            WindowHandler.switch_panel(root)
        except Exception as error:
            logger.error(f"Error handling Back button click: {error}", exc_info=True)
