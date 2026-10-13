from gui.frames.Main import Main
from logger import get_logger
from logic.Settings import cache

logger = get_logger("App")
logger.info("Application starting...")

# Show the main frame
main = Main()