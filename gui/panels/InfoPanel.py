from tkinter import Frame, Label
from ..components.BackButton import BackButton
from logic.DeviceInfo import DeviceInfo
from logger import get_logger

logger = get_logger("InfoPanel")


class InfoPanel(Frame):
    """Panel displaying device information with styled cards and Back button navigation."""
    def __init__(self, root):
        super().__init__(root, padx=30, pady=25)
        logger.info("Initializing InfoPanel")

        # initialize our logic class
        info = DeviceInfo()

        # Header Title
        self.title_label = Label(
            self,
            text="Device Information",
            font=("Arial", 22, "bold"),
            fg="#1a365d",
        )
        self.title_label.pack(pady=(5, 20))

        # Main Info Card Container
        self.card_frame = Frame(
            self,
            bg="#f8fafc",
            bd=1,
            relief="solid",
            padx=25,
            pady=20,
        )
        self.card_frame.pack(fill="x", padx=10, pady=10)

        # Device info rows
        self._add_info_row("Hostname:", info.hostname)
        self._add_info_row("IP Address:", info.ipAddress)
        self._add_info_row("Network Interfaces:", info.networkInterfaces)

        # Back Button to return to main menu panel
        self.back_button = BackButton(self)
        self.back_button.pack(pady=(30, 10))

    def _add_info_row(self, label_text, value_text):
        """Helper to create a formatted information row with aligned badge."""
        row_frame = Frame(self.card_frame, bg="#f8fafc")
        row_frame.pack(fill="x", pady=8, anchor="w")

        field_label = Label(
            row_frame,
            text=label_text,
            font=("Arial", 14, "bold"),
            fg="#2d3748",
            bg="#f8fafc",
            width=18,
            anchor="w",
        )
        field_label.pack(side="left")

        val_frame = Frame(row_frame, bg="#edf2f7", padx=12, pady=5, bd=1, relief="groove")
        val_frame.pack(side="left", fill="x", expand=True)

        value_label = Label(
            val_frame,
            text=str(value_text),
            font=("Arial", 14),
            fg="#1a202c",
            bg="#edf2f7",
            anchor="w",
        )
        value_label.pack(side="left")
