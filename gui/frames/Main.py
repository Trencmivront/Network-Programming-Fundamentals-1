import tkinter as tk
from ..panels.MainButtonSetPanel import MainButtonSetPanel
from logger import get_logger, attach_gui_error_handler
from logic.GlobalExceptionHandler import GlobalExceptionHandler
import logic.WindowHandler as WindowHandler

logger = get_logger("Main")

class Main(tk.Tk):
    def __init__(self):
        super().__init__()

        # Attach GUI error dialog handler
        attach_gui_error_handler(self)

        # Catch all unhandled exceptions and route them through the logger
        GlobalExceptionHandler(self).install()

        self.option_add("*Font", "Arial 16")  # family and size
        self.title("Project - 1")
        self.geometry("800x600")

        self.current_panel = None
        WindowHandler.switch_panel(root=self, panel_class=MainButtonSetPanel)
        self.mainloop()
