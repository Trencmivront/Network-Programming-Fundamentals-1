from gui.frames.Main import Main
from logger import get_logger
import os

logger = get_logger("App")
logger.info("Application starting...")

# Check if settings file exists at app start
if os.path.isfile("settings.json"):
    logger.info("Initializing the settings file...")
    try:
        import logic.Settings as sett
        sett.init()
    except Exception as e:
        logger.error("Error while initializing settings file : %s", e)

# Show the main frame
main = Main()
main.mainloop()