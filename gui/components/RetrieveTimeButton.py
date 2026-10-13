from tkinter import Button
from logger import get_logger

logger = get_logger("RetrieveTimeButton")


class RetrieveTimeButton(Button):
    def __init__(self, master):
        super().__init__(master, text="Retrieve Current Time", width=20)
        self.config(command=self.on_click)

    def on_click(self):
        try:
            logger.info("RetrieveTimeButton clicked - navigating to RetrieveTimePanel")
            from ..panels.RetrieveTimePanel import RetrieveTimePanel
            root = self.winfo_toplevel()
            if hasattr(root, "switch_panel"):
                root.switch_panel(RetrieveTimePanel)
        except Exception as error:
            logger.error(f"Error opening RetrieveTimePanel: {error}", exc_info=True)