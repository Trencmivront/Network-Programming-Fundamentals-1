from tkinter import Frame, Label, Button, Entry, StringVar, messagebox
from ..components.BackButton import BackButton
from logger import get_logger
from logic.WindowHandler import switch_panel

logger = get_logger("ChatClientConnectPanel")


class ChatClientConnectPanel(Frame):
    def __init__(self, root):
        super().__init__(root, padx=20, pady=20)
        logger.info("Initializing ChatClientCChatClientConnectPanelonnect panel")

        # Title
        self.title_label = Label(self, text="Chat Client Connect", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=(0, 15))

        # Inputs frame
        self.inputs_frame = Frame(self)
        self.inputs_frame.pack(fill="x", expand=False, pady=10)

        self.hostname_var = StringVar(value="localhost")
        self.port_var = StringVar(value="8080")
        self.username_var = StringVar(value="Client")

        # Username entry
        self.username_row = Frame(self.inputs_frame)
        self.username_row.pack(fill="x", pady=4)
        Label(self.username_row, text="Username:", font=("Arial", 11, "bold"), width=10, anchor="w").pack(side="left")
        self.username_entry = Entry(self.inputs_frame, textvariable=self.username_var)
        self.username_entry.pack(in_=self.username_row, side="left", fill="x", expand=True)

        # Hostname entry
        self.hostname_row = Frame(self.inputs_frame)
        self.hostname_row.pack(fill="x", pady=4)
        Label(self.hostname_row, text="Hostname:", font=("Arial", 11, "bold"), width=10, anchor="w").pack(side="left")
        self.hostname_entry = Entry(self.inputs_frame, textvariable=self.hostname_var)
        self.hostname_entry.pack(in_=self.hostname_row, side="left", fill="x", expand=True)

        # Port number entry
        self.port_row = Frame(self.inputs_frame)
        self.port_row.pack(fill="x", pady=4)
        Label(self.port_row, text="Port:", font=("Arial", 11, "bold"), width=10, anchor="w").pack(side="left")
        self.port_entry = Entry(self.inputs_frame, textvariable=self.port_var)
        self.port_entry.pack(in_=self.port_row, side="left", fill="x", expand=True)

        # Buttons frame
        self.buttons_frame = Frame(self)
        self.buttons_frame.pack(pady=15)

        # Start Chat button
        self.start_chat_button = Button(
            self.buttons_frame,
            text="Start Chat",
            width=15,
            command=self.start_chat,
            font=("Arial", 11, "bold"),
        )
        self.start_chat_button.pack(pady=5)

        # Back button
        self.back_button = BackButton(self.buttons_frame)
        self.back_button.pack(pady=5)

    def start_chat(self):
        """Validates connection inputs, checks client connection, logs errors, and transitions to ChatClientPanel."""

        username = self.username_entry.get().strip()
        host = self.hostname_entry.get().strip()
        port_raw = self.port_entry.get().strip()

        # Validate inputs
        if not host:
            err_msg = "Hostname cannot be empty."
            logger.error("Client connection error: %s", err_msg)
            messagebox.showerror("Invalid Input", err_msg)
            return

        try:
            port = int(port_raw)
            if not (1 <= port <= 65535):
                raise ValueError("Port must be between 1 and 65535.")
        except ValueError as err:
            err_msg = f"Invalid port number '{port_raw}': {err}"
            logger.error("Client connection error: %s", err_msg)
            messagebox.showerror("Invalid Input", err_msg)
            return

        # Open ChatClientPanel
        try:
            from .ChatClientPanel import ChatClientPanel
            root = self.winfo_toplevel()
            switch_panel(root, ChatClientPanel, username=username, host=host, port=port)
        except Exception as error:
            logger.error("Error opening ChatClientPanel: %s", error, exc_info=True)