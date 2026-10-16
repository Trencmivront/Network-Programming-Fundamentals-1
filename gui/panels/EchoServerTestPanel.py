from tkinter import Frame, Label, Button, Text, Scrollbar, END
from logger import get_logger
from time import ctime
from logic.EchoServerTest import echo_server
import threading

logger = get_logger("EchoServerTestPanel")

class EchoServerTestPanel(Frame):
    def __init__(self, root):
        super().__init__(root, padx=20, pady=20)
        logger.info("Initializing EchoServerTestPanel")

        self.seconds_elapsed = 0
        self.timer_running = False
        self._timer_job = None
        # This boolean condition used in echo_server function to check when to stop the function
        self.isThreadRunning = False
        # Initializing the backgroun daemon for running server
        self.thread = threading.Thread(target=echo_server, args=(self.on_data, self.is_thread_running), daemon=True)

        # Title
        self.title_label = Label(self, text="Echo Server Test", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=(0, 10))

        # Counter showing how long the server has been running
        self.timer_frame = Frame(self)
        self.timer_frame.pack(pady=5)
        self.timer_desc_label = Label(self.timer_frame, text="Server Running Time: ", font=("Arial", 14, "bold"))
        self.timer_desc_label.pack(side="left")
        self.timer_label = Label(self.timer_frame, text="00:00:00", font=("Arial", 14), fg="darkgreen")
        self.timer_label.pack(side="left")

        # Received data display section
        self.data_section_label = Label(self, text="Received Data:", font=("Arial", 14, "bold"))
        self.data_section_label.pack(anchor="w", pady=(15, 5))

        # Text area with scrollbar to display received data
        self.log_frame = Frame(self)
        self.log_frame.pack(fill="both", expand=True, pady=5)

        self.scrollbar = Scrollbar(self.log_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.data_display = Text(
            self.log_frame,
            height=8,
            width=50,
            yscrollcommand=self.scrollbar.set,
            font=("Arial", 12),
            state="disabled",
        )
        self.data_display.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.data_display.yview)

        # Back button to return specifically to EchoPanel
        self.back_button = Button(self, text="Back", width=15, command=self.on_back)
        self.back_button.pack(pady=(15, 0))

        # Start the running counter
        self.start_timer()
        # start thread
        try:
            self.isThreadRunning = True
            self.thread.start()
        except Exception as error:
            logger.error("Error for echo server test daemon: %s", error)

    def start_timer(self):
        """Starts the uptime counter."""
        if not self.timer_running:
            self.timer_running = True
            self._update_timer()

    def stop_timer(self):
        """Stops the uptime counter and cancels any scheduled after callbacks."""
        """ Also sets the thread state to stopped"""
        self.timer_running = False
        self.isThreadRunning = False
        if self._timer_job:
            self.after_cancel(self._timer_job)
            self._timer_job = None

    def _update_timer(self):
        """Ticks every second to update the elapsed time display."""
        if self.timer_running:
            hours = self.seconds_elapsed // 3600
            minutes = (self.seconds_elapsed % 3600) // 60
            seconds = self.seconds_elapsed % 60
            self.timer_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            self.seconds_elapsed += 1
            # asynchronous non blocking function callback
            self._timer_job = self.after(1000, self._update_timer)

    def display_received_data(self, data_str):
        """Method to display received data on the panel."""
        self.data_display.config(state="normal")
        self.data_display.insert(END, f"{ctime() + " :" +  data_str}\n")
        self.data_display.see(END)
        self.data_display.config(state="disabled")

    def on_back(self):
        """Cancels timer and switches view back to EchoPanel."""
        try:
            logger.info("EchoServerTestPanel: Back button clicked - returning to EchoPanel")
            self.stop_timer()
            from .EchoPanel import EchoPanel
            root = self.winfo_toplevel()
            if hasattr(root, "switch_panel"):
                root.switch_panel(EchoPanel)
        except Exception as error:
            logger.error(f"Error navigating back to EchoPanel: {error}", exc_info=True)

    def destroy(self):
        """Cleanup timer when widget is destroyed."""
        self.stop_timer()
        super().destroy()

    def on_data(self, data):
        """ Decodes and displays data sent from client"""
        # decode the returned data from server
        text = data.decode("utf-8", errors="replace") if isinstance(data, bytes) else str(data)
        # Display the data on UI
        self.after(0, self.display_received_data, text)

    def is_thread_running(self):
        """Returns the current state of thread"""
        return self.isThreadRunning
