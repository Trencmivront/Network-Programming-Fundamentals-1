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

# check if logging and debuggin is enabled or not
loggingEnabled = True
debuggingEnabled = False

class AppLogsFilter(logging.Filter):
    """Filter that allows only non-error log records (DEBUG, INFO, WARNING)."""
    def filter(self, record):
        return record.levelno < logging.ERROR

from logic.DebugLogHandler import DebugLogHandler

_configured = False
_app_handler = None
_error_handler = None
_debug_handler = None

# we set up values in base logger.
_root_logger = logging.getLogger()
_root_logger.setLevel(logging.DEBUG)

def setup_logging():
    """Configures the logging system with separated app and error logs.
    
    app_handler writes into default log file while error_handler writes into error log file.
    This makes easier to read application errors when needed and if there are any.
    """

    global _configured, _app_handler, _error_handler, _debug_handler, _root_logger
    if _configured:
        return
    _configured = True

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler for app logs (DEBUG, INFO, WARNING only)
    _app_handler = RotatingFileHandler(
        APP_LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    _app_handler.setLevel(logging.INFO if loggingEnabled else logging.CRITICAL + 1)
    # Filter for app_handler because it won't write error logs.
    _app_handler.addFilter(AppLogsFilter())
    _app_handler.setFormatter(formatter)
    # Adding log handler object. It writes logs into selected file.
    _root_logger.addHandler(_app_handler)

    # File handler for error logs (ERROR and CRITICAL only)
    _error_handler = RotatingFileHandler(
        ERROR_LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    _error_handler.setLevel(logging.ERROR if loggingEnabled else logging.CRITICAL + 1)
    _error_handler.setFormatter(formatter)
    _root_logger.addHandler(_error_handler)

    # Debug window handler
    _debug_handler = DebugLogHandler()
    _debug_handler.setLevel(logging.DEBUG)
    _debug_handler.setFormatter(formatter)
    _root_logger.addHandler(_debug_handler)


def set_file_logging(enabled: bool):
    """Enable or disable writing to log files by adjusting log levels."""
    global loggingEnabled
    loggingEnabled = bool(enabled)
    setup_logging()
    if _app_handler and _error_handler:
        if loggingEnabled:
            # Start file outputs
            _app_handler.setLevel(logging.INFO)
            _error_handler.setLevel(logging.ERROR)
        else:
            # Setting level above CRITICAL stops all file output
            _app_handler.setLevel(logging.CRITICAL + 1)
            _error_handler.setLevel(logging.CRITICAL + 1)

def set_debugging(enabled: bool):
    """Enable or disable debug window display."""
    global debuggingEnabled
    debuggingEnabled = bool(enabled)


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
