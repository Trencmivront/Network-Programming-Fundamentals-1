import tkinter as tk
from ..panels.MainButtonSetPanel import MainButtonSetPanel
from logger import get_logger, attach_gui_error_handler
from logic.GlobalExceptionHandler import GlobalExceptionHandler

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
        self.show_main_panel()
        self.mainloop()


    def show_main_panel(self):
        """Displays the main button menu panel."""
        logger.info("Switching to MainButtonSetPanel")
        self.switch_panel(MainButtonSetPanel)

    def switch_panel(self, panel_class, *args, **kwargs):
        """Replaces the current panel with an instance of panel_class."""
        try:
            self.old_panel = self.current_panel
            logger.info(f"Switching panel to {panel_class.__name__}")
            
            # Show loading state
            loading_label = tk.Label(self, text="Loading...", font=("Arial", 14))
            loading_label.pack(expand=True)
            self.update()  # Force GUI refresh
            
            # Create panel in background
            import threading
            def create_panel():
                # Destroy panel on the background because it takes so much time
                if self.old_panel is not None:
                    self.old_panel.destroy()
                    # Create new panel
                self.current_panel = panel_class(self, *args, **kwargs)

                if(self.current_panel is None):
                    self.switch_panel(MainButtonSetPanel)
                    return

                self.after(0, lambda: (
                    loading_label.destroy(),
                    self.current_panel.pack(expand=True),
                    logger.info(f"Panel {panel_class.__name__} loaded")
                ))
            
            thread = threading.Thread(target=create_panel, daemon=True)
            thread.start()
            
        except Exception as error:
            logger.error(f"Error switching panel to {panel_class.__name__}: {error}", exc_info=True)
