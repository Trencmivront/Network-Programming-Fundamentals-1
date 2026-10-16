import logging
from tkinter import messagebox


class GlobalErrorDisplayHandler(logging.Handler):
    """A logging handler that displays ERROR and CRITICAL log records as a Tkinter dialog.

    Attach this handler to the root logger so that any logger.error() or
    logger.critical() call anywhere in the application automatically shows a
    modal error message box to the user.

    :param root_window: The Tk root window used to schedule dialogs.
    """

    def __init__(self, root_window):
        super().__init__(level=logging.ERROR)
        self.root_window = root_window

    def emit(self, record):
        try:
            msg = self.format(record)
            self.root_window.after(
                0,
                lambda m=msg: messagebox.showerror("Application Error", m),
            )
        except Exception:
            self.handleError(record)
