from tkinter import Frame, Label, Button, Text, Scrollbar, Entry, StringVar, IntVar,  END
from time import ctime
from logger import get_logger
from logic.EchoClientTest import EchoClientTest
from ..components.BackButton import BackButton
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

        self.hostname_var = StringVar()
        self.port_var = StringVar()
        self.message_var = StringVar()

        # Hostname entry
        self.hostname_row = Frame(self.inputs_frame)
        self.hostname_row.pack(fill="x", pady=3)
        Label(self.hostname_row, text="Hostname:", font=("Arial", 11, "bold"), width=10, anchor="w").pack(side="left")
        self.hostname_entry = Entry(self.inputs_frame, textvariable=self.hostname_var)
        self.hostname_entry.pack(in_=self.hostname_row, side="left", fill="x", expand=True)

        # Port number entry
        self.port_row = Frame(self.inputs_frame)
        self.port_row.pack(fill="x", pady=3)
        Label(self.port_row, text="Port:", font=("Arial", 11, "bold"), width=10, anchor="w").pack(side="left")
        self.port_entry = Entry(self.inputs_frame, textvariable=self.port_var)
        self.port_entry.pack(in_=self.port_row, side="left", fill="x", expand=True)

        # Message entry
        self.message_row = Frame(self.inputs_frame)
        self.message_row.pack(fill="x", pady=3)
        Label(self.message_row, text="Message:", font=("Arial", 11, "bold"), width=10, anchor="w").pack(side="left")
        self.message_entry = Entry(self.inputs_frame, textvariable=self.message_var)
        self.message_entry.pack(in_=self.message_row, side="left", fill="x", expand=True)

        # Button to send with values
        self.send_button = Button(self.inputs_frame, text="Send", width=10,
                                  command=lambda: self.start_client(self.hostname_entry.get(),
                                                            self.port_entry.get(),
                                                            self.message_entry.get()))
        self.send_button.pack(pady=8)
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
        self.data_display.tag_config("match", foreground="green")
        self.data_display.tag_config("not_match", foreground="red")

        self.data_display.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.data_display.yview)

        # Stop the running thread before changing panel
        self.back_button = BackButton(self)
        self.back_button.config(command=lambda: (self.stop_thread(), self.back_button.on_click()))
        self.back_button.pack(pady=(15, 0))


    def start_client(self, host, port, message):
        # set the message globally to check later
        self.message = message
        # Initialize client object
        try:
            client = EchoClientTest(host=host, port=int(port))
            if(client is None):
                logger.error("Could not initialize the client.")
                return
        except Exception as e:
            logger.error("Echo client initializing error %s", e)
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
        # checking if returned data is the same
        is_match = (data_str == self.message)
        match_text = "(match)" if is_match else "(not match)"
        match_tag = "match" if is_match else "not_match"

        self.data_display.config(state="normal")
        self.data_display.insert(END, f"{ctime()} ")
        self.data_display.insert(END, match_text, match_tag)
        self.data_display.insert(END, f": {data_str}\n")
        self.data_display.see(END)
        self.data_display.config(state="disabled")


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