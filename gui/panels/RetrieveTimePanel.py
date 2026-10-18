from tkinter import Frame, Label
from ..components.BackButton import BackButton
from logger import get_logger
from time import ctime
from logic.SNTP import SNTP

logger = get_logger("RetrieveTimePanel")

class RetrieveTimePanel(Frame):

    def __init__(self, root):
        super().__init__(root, padx=20, pady=20)
        logger.info("Initializing RetrieveTimePanel")

        local_time = ctime()
        try:
            sntp = SNTP()
        except Exception as e:
            # exit from function if exception occours
            self.destroy()
            return
        server_time = sntp.timestamp

        # Title
        self.title_label = Label(self, text="Retrieve Time", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=(10, 20))

        # UI container for Server Time
        self.server_time_frame = Frame(self)
        self.server_time_frame.pack(pady=8, anchor="center")
        self.server_time_label = Label(self.server_time_frame, text="Server Time: ", font=("Arial", 16, "bold"))
        self.server_time_label.pack(side="left")
        self.server_time_display = Label(self.server_time_frame, text=f"{server_time}", font=("Arial", 16))
        self.server_time_display.pack(side="left")

        # UI container for Local Time
        self.local_time_frame = Frame(self)
        self.local_time_frame.pack(pady=8, anchor="center")
        self.local_time_label = Label(self.local_time_frame, text="Local Time: ", font=("Arial", 16, "bold"))
        self.local_time_label.pack(side="left")
        self.local_time_display = Label(self.local_time_frame, text=f"{local_time}", font=("Arial", 16))
        self.local_time_display.pack(side="left")

        # Back button to return to main panel
        self.back_button = BackButton(self)
        self.back_button.pack(pady=(25, 10))
