import sys
import threading
from logger import get_logger

logger = get_logger("GlobalException")


class GlobalExceptionHandler:
    """Catches all unhandled exceptions across the main thread and 
    displays them in a pop-up window

    Every unhandled exception that reaches this class will also be shown
    automatically as a Tkinter error dialog.

    Usage
    -----
    Call ``GlobalExceptionHandler.install(root)`` once, passing the Tk root
    window, right after the window is created.

    :param root_window: The Tk root window (used for Tkinter's
                        report_callback_exception hook).
    """

    def __init__(self, root_window):
        self.root_window = root_window

    def handle(self, exc_type, exc_value, exc_traceback):
        """Unified handler: logs the exception and lets the root logger
        (and any attached GUI handler) take care of display."""
        if issubclass(exc_type, KeyboardInterrupt):
            # Let Python handle Ctrl+C normally
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.error(
            "Unhandled exception",
            exc_info=(exc_type, exc_value, exc_traceback),
        )

    def install(self):
        """Register this handler for all three exception pathways."""
        # 1. Main-thread unhandled exceptions
        sys.excepthook = self.handle

        # 2. Background-thread unhandled exceptions (Python 3.8+)
        threading.excepthook = lambda args: self.handle(
            args.exc_type, args.exc_value, args.exc_traceback
        )

        # 3. Tkinter UI callback exceptions (button clicks, bindings, after(), …)
        self.root_window.report_callback_exception = self.handle
