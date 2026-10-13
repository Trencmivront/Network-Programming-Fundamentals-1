from tkinter import Frame, Label
from ..components.BackButton import BackButton
from logger import get_logger

logger = get_logger("SettingsPanel")


class SettingsPanel(Frame):
    def __init__(self, root):
        super().__init__(root, padx=20, pady=20)
        logger.info("Initializing SettingsPanel")

        # Title placeholder for Settings (panel can stay empty for now as requested)
        self.title_label = Label(self, text="Settings", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=(10, 20))

        # Back button to return to main panel
        self.back_button = BackButton(self)
        self.back_button.pack(pady=(25, 10))
