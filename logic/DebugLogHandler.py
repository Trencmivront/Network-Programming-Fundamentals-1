import logging
import tkinter as tk


class DebugLogHandler(logging.StreamHandler):
    """Custom log handler that forwards formatted log messages to the GUI debug window."""

    def emit(self, record):
        try:
            from gui.frames.Main import Main

            instance = Main.get_instance()
            if instance is None:
                return

            debug_window = getattr(instance, "debug", None)
            if debug_window is not None:
                try:
                    if debug_window.winfo_exists():
                        msg = self.format(record)
                        debug_window.after(0, lambda m=msg: debug_window.display_log(m))
                except (tk.TclError, AttributeError):
                    pass
        except Exception:
            self.handleError(record)
        finally:
            # I also want to see logs in command line
            super().emit(record=record)