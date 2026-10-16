from tkinter import Button
from logger import get_logger

logger = get_logger("SettingsButton")


class SettingsButton(Button):
    def __init__(self, master):
        super().__init__(master, text="Settings", width=20)
        self.config(command=self.on_click)

    def on_click(self):
        try:
            from ..panels.SettingsPanel import SettingsPanel
            root = self.winfo_toplevel()
            if hasattr(root, "switch_panel"):
                root.switch_panel(SettingsPanel)
        except Exception as error:
            logger.error(f"Error opening SettingsPanel: {error}", exc_info=True)
