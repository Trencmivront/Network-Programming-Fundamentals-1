from tkinter import Frame, Label, Button, Text, Scrollbar, Entry, StringVar, IntVar,  END
from logger import get_logger
from logic.EchoClientTest import EchoClientTest
import threading
logger = get_logger("EchoClientTestPanel")

class EchoClientTestPanel(Frame):
    def __init__(self, root):
        super().__init__(root, padx=20, pady=20)
        logger.info("Initializing EchoClientTestPanel")

        self.isThreadRunning = False

        # Title
        self.title_label = Label(self, text="Echo Client Test", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=(0, 10))

        # Options section
        self.options_section_label = Label(self, text="Options", font=("Arial", 14, "bold"))
        self.options_section_label.pack(anchor="center", pady=(15, 5))

        # input fields and button
        self.inputs_frame = Frame(self)
        self.inputs_frame.pack(fill="both", expand=False, pady=5)

        hostname_var = StringVar
        port_var = IntVar
        message_var = StringVar
        # TODO: create label or placeholder for input fields
        # Hostname entry
        self.hostname_entry = Entry(self.inputs_frame, textvariable=hostname_var)
        self.hostname_entry.pack(pady=5)

        # Port number entry
        self.port_entry = Entry(self.inputs_frame, textvariable=port_var)
        self.port_entry.pack(pady=5)

        # Message entry
        self.message_entry = Entry(self.inputs_frame, textvariable=message_var)
        self.message_entry.pack(pady=5)

        # Button to send with values
        self.send_button = Button(self.inputs_frame, text="Send",
                                  command=lambda: self.start_client(self.hostname_entry.get(),
                                                            self.port_entry.get(),
                                                            self.message_entry.get()))
        self.send_button.pack(pady=5)
        # Received data display section
        self.data_section_label = Label(self, text="Received Data:", font=("Arial", 14, "bold"))
        self.data_section_label.pack(anchor="w", pady=(15, 5))

        # Text area with scrollbar to display received data
        self.recv_frame = Frame(self)
        self.recv_frame.pack(fill="both", expand=True, pady=5)

        self.scrollbar = Scrollbar(self.recv_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.data_display = Text(
            self.recv_frame,
            height=8,
            width=50,
            yscrollcommand=self.scrollbar.set,
            font=("Arial", 12),
            state="disabled"
        )

        self.data_display.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.data_display.yview)
        
        # Back button to return specifically to EchoPanel
        self.back_button = Button(self, text="Back", width=15, command=self.on_back)
        self.back_button.pack(pady=(15, 0))

    def start_client(self, host, port, message):
        # Initialize client object
        client = EchoClientTest(host=host, port=int(port))
        if(client is None):
            logger.error("Could not initialize the client.")
            return
        # Initializing the backgroun daemon for running server
        self.thread = threading.Thread(target=client.send_message, args=(message, self.on_data, self.is_thread_running), daemon=True)
        # start thread
        try:
            self.isThreadRunning = True
            self.thread.start()
        except Exception as error:
            logger.error("Error for echo client test daemon: %s", error)

    def stop_thread(self):
        """ Sets the thread state to stopped."""
        self.isThreadRunning = False

    def display_received_data(self, data_str):
        """Method to display received data on the panel."""
        self.stop_thread()
        self.data_display.config(state="normal")
        self.data_display.insert(END, f"{data_str}\n")
        self.data_display.see(END)
        self.data_display.config(state="disabled")

    def on_back(self):
        """Cancels timer and switches view back to EchoPanel."""
        try:
            logger.info("Returning to EchoPanel")
            self.stop_thread()
            from .EchoPanel import EchoPanel
            root = self.winfo_toplevel()
            if hasattr(root, "switch_panel"):
                root.switch_panel(EchoPanel)
        except Exception as error:
            logger.error(f"Error navigating back to EchoPanel: {error}", exc_info=True)

    def destroy(self):
        """Cleanup timer when widget is destroyed."""
        self.stop_thread()
        super().destroy()

    def on_data(self, data):
        """ Decodes and displays data returned from server running in thread """
        # decode the returned data from server
        text = data.decode("utf-8", errors="replace") if isinstance(data, bytes) else str(data)
        # Display the data on UI
        self.after(0, self.display_received_data, text)

    def is_thread_running(self):
        """Returns the current state of thread"""
        return self.isThreadRunning