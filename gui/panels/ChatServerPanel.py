from tkinter import Frame, Label, Button, Text, Scrollbar, Entry, StringVar, END
from ..components.BackButton import BackButton
from logic.ChatServer import ChatServer as CS
from logger import get_logger

logger = get_logger("ChatServerPanel")

class ChatServerPanel(Frame):
    def __init__(self, root):
        super().__init__(root, padx=20, pady=20)
        logger.info("Initializing ChatServerPanel")

        self.server = None # error checking for later

        try:
            self.server = CS()
        except Exception:
            self.destroy()
            raise

        self.server.on_receive(self.display_message)
        self.server.start()

        # Title
        self.title_label = Label(self, text="Chat Server", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=(0, 10))

        # Status label
        self.status_label = Label(
            self,
            text=f"Server Status: Listening on {self.server.host}:{self.server.port}",
            font=("Arial", 11),
            fg="#2b6cb0",
        )
        self.status_label.pack(pady=(0, 10))

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
        self.message_entry.bind("<Return>", lambda event: self.send_message())

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

    def destroy(self):
        if self.server is not None:
            self.server.close()
        return super().destroy()

    def send_message(self):
        """Sends a message from server to all connected clients."""
        message = self.message_var.get().strip()
        if not message:
            return
        logger.info("Server message to send: %s", message)

        if self.server is not None:
            msg = self.server.message(message)

        if msg:
            self.display_message(f"{msg}")
        self.message_var.set("")

    def display_message(self, message_str):
        """Displays a message in the chat window (thread-safe)."""
        def _insert():
            try:
                if self.winfo_exists():
                    self.chat_display.config(state="normal")
                    self.chat_display.insert(END, f"{message_str}\n")
                    self.chat_display.see(END)
                    self.chat_display.config(state="disabled")
            except Exception:
                pass

        self.after(0, _insert)
