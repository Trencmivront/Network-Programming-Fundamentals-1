import os
import logging
from logging.handlers import RotatingFileHandler

# Project directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Ensure the logs directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# the location of log files
APP_LOG_FILE = os.path.join(LOG_DIR, "app.log")
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")


class AppLogsFilter(logging.Filter):
    """Filter that allows only non-error log records (DEBUG, INFO, WARNING)."""
    def filter(self, record):
        return record.levelno < logging.ERROR

_configured = False

def setup_logging():
    """Configures the logging system with separated app and error logs.
    
    app_handler writes into default log file while error_handler writes into error log file.
    This makes easier to read application errors when needed and if there are any.
    """

    global _configured
    if _configured:
        return
    _configured = True

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # we set up values in base logger.
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # File handler for app logs (DEBUG, INFO, WARNING only)
    app_handler = RotatingFileHandler(
        APP_LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    app_handler.setLevel(logging.INFO)
    # Filter for app_handler because it won't write error logs.
    app_handler.addFilter(AppLogsFilter())
    app_handler.setFormatter(formatter)
    # Adding log handler object. It writes logs into selected file.
    root_logger.addHandler(app_handler)

    # File handler for error logs (ERROR and CRITICAL only)
    error_handler = RotatingFileHandler(
        ERROR_LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    root_logger.addHandler(error_handler)

    # Stream handler for console output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)


def get_logger(name=None):
    """Retrieve a configured logger."""
    setup_logging()
    # return the configured logger
    return logging.getLogger(name if name else "app")


def attach_gui_error_handler(root_window):
    """Attach a GUI error-dialog handler to the root logger.

    Must be called after the Tk root window has been created.
    Any subsequent logger.error() / logger.critical() call anywhere in the
    application will then also pop up a Tkinter messagebox.

    :param root_window: The Tk root window.
    """
    from logic.GlobalErrorDisplayHandler import GlobalErrorDisplayHandler

    formatter = logging.Formatter(
        "[%(name)s]: %(message)s",
    )
    handler = GlobalErrorDisplayHandler(root_window)
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)


# Initialize logging immediately on import
setup_logging()
app_logger = get_logger("app")
error_logger = get_logger("error")
