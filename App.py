from gui.frames.Main import Main
from logger import get_logger

logger = get_logger("App")
logger.info("Application starting...")

# Show the main frame
main = Main()