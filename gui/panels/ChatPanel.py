from tkinter import Frame, Label, Button
from ..components.BackButton import BackButton
from logger import get_logger
from logic.WindowHandler import switch_panel

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
        self.server_button = Button(
            self.role_button_frame, text="Server", width=12, command=self.open_server_panel
        )
        self.server_button.pack(side="left", padx=10)

        self.client_button = Button(
            self.role_button_frame, text="Client", width=12, command=self.open_client_panel
        )
        self.client_button.pack(side="left", padx=10)

        # Back button to return to main panel
        self.back_button = BackButton(self)
        self.back_button.pack(pady=(25, 10))

    def open_server_panel(self):
        try:
            logger.info("Opening chat server panel.")
            from .ChatServerPanel import ChatServerPanel
            root = self.winfo_toplevel()
            switch_panel(root, ChatServerPanel)
        except Exception as error:
            logger.error(f"Error opening ChatServerPanel: {error}", exc_info=True)

    def open_client_panel(self):
        try:
            logger.info("Opening chat client connect panel.")
            from .ChatClientConnectPanel import ChatClientConnectPanel
            root = self.winfo_toplevel()
            switch_panel(root, ChatClientConnectPanel)
        except Exception as error:
            logger.error(f"Error opening ChatClientConnect: {error}", exc_info=True)

