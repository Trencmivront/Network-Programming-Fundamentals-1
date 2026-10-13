import tkinter as tk
from ..panels.MainButtonSetPanel import MainButtonSetPanel
from logger import get_logger

logger = get_logger("Main")


class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add("*Font", "Arial 16")  # family and size
        self.title("Project - 1")
        self.geometry("800x600")

        self.current_panel = None
        self.show_main_panel()
        self.mainloop()

    def show_main_panel(self):
        """Displays the main button menu panel."""
        logger.info("Switching to MainButtonSetPanel")
        self.switch_panel(MainButtonSetPanel)

    def switch_panel(self, panel_class, *args, **kwargs):
        """Replaces the current panel with an instance of panel_class."""
        try:
            if self.current_panel is not None:
                self.current_panel.destroy()
            logger.info(f"Switching panel to {panel_class.__name__}")
            self.current_panel = panel_class(self, *args, **kwargs)
            self.current_panel.pack(expand=True)
            return self.current_panel
        except Exception as error:
            logger.error(f"Error switching panel to {panel_class.__name__}: {error}", exc_info=True)
