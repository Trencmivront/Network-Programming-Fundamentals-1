from tkinter import Button
from logger import get_logger

logger = get_logger("ChatButton")


class ChatButton(Button):
    def __init__(self, master):
        super().__init__(master, text="Chat", width=20)
        self.config(command=self.on_click)

    def on_click(self):
        try:
            logger.info("ChatButton clicked - navigating to ChatPanel")
            from ..panels.ChatPanel import ChatPanel
            root = self.winfo_toplevel()
            if hasattr(root, "switch_panel"):
                root.switch_panel(ChatPanel)
        except Exception as error:
            logger.error(f"Error opening ChatPanel: {error}", exc_info=True)