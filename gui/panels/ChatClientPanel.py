from tkinter import Frame, Label, Button, Text, Scrollbar, Entry, StringVar, END
from ..components.BackButton import BackButton
from logger import get_logger

logger = get_logger("ChatClientPanel")


class ChatClientPanel(Frame):
    def __init__(self, root, host="localhost", port=8080):
        super().__init__(root, padx=20, pady=20)
        self.host = host
        self.port = port
        logger.info("Initializing ChatClientPanel (host=%s, port=%s)", host, port)

        # Title
        self.title_label = Label(self, text="Chat Client", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=(0, 10))

        # Connection target label
        self.info_label = Label(
            self,
            text=f"Target: {self.host}:{self.port} (Logic to be implemented)",
            font=("Arial", 11),
            fg="gray",
        )
        self.info_label.pack(pady=(0, 10))

        # Chat display area
        self.chat_frame = Frame(self)
        self.chat_frame.pack(fill="both", expand=True, pady=5)

        self.scrollbar = Scrollbar(self.chat_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.chat_display = Text(
            self.chat_frame,
            height=10,
            width=50,
            yscrollcommand=self.scrollbar.set,
            font=("Arial", 12),
            state="disabled",
        )
        self.chat_display.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.chat_display.yview)

        # Message input area
        self.input_frame = Frame(self)
        self.input_frame.pack(fill="x", pady=10)

        self.message_var = StringVar()
        self.message_entry = Entry(self.input_frame, textvariable=self.message_var, font=("Arial", 12))
        self.message_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.send_button = Button(
            self.input_frame,
            text="Send",
            width=10,
            command=self.send_message,
            font=("Arial", 11, "bold"),
        )
        self.send_button.pack(side="right")

        # Back button
        self.back_button = BackButton(self)
        self.back_button.pack(pady=(15, 0))

    def send_message(self):
        """Sends a message from client. Logic to be added later."""
        message = self.message_var.get().strip()
        if not message:
            return
        logger.info("Client message to send: %s", message)
        # TODO: Implement client send logic
        self.display_message(f"Client: {message}")
        self.message_var.set("")

    def display_message(self, message_str):
        """Displays a message in the chat window."""
        self.chat_display.config(state="normal")
        self.chat_display.insert(END, f"{message_str}\n")
        self.chat_display.see(END)
        self.chat_display.config(state="disabled")

    # TODO: Add client networking logic (connect, send, receive) later
