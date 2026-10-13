from tkinter import Frame, Label, Button
from ..components.BackButton import BackButton
from logger import get_logger

logger = get_logger("ChatPanel")


class ChatPanel(Frame):
    def __init__(self, root):
        super().__init__(root, padx=20, pady=20)
        logger.info("Initializing ChatPanel")

        # Top label: "This computer is:"
        self.header_label = Label(self, text="This computer is:", font=("Arial", 16, "bold"))
        self.header_label.pack(pady=(10, 15))

        # Container frame for buttons side by side
        self.role_button_frame = Frame(self)
        self.role_button_frame.pack(pady=10)

        # "Server" and "Client" buttons side by side
        self.server_button = Button(self.role_button_frame, text="Server", width=12)
        self.server_button.pack(side="left", padx=10)

        self.client_button = Button(self.role_button_frame, text="Client", width=12)
        self.client_button.pack(side="left", padx=10)

        # Back button to return to main panel
        self.back_button = BackButton(self)
        self.back_button.pack(pady=(25, 10))
