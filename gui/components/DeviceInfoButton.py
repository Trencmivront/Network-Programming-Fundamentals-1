from tkinter import Button
from logger import get_logger

logger = get_logger("DeviceInfoButton")


# Set of predefined classes for main menu buttons
class DeviceInfoButton(Button):
    """A button that navigates to InfoPanel when clicked.

    :param master: Container frame for the button.
    """
    def __init__(self, master):
        super().__init__(master, text="Device Info", width=20)
        self.config(command=self.on_click)

    def on_click(self):
        try:
            logger.info("DeviceInfoButton clicked - navigating to InfoPanel")
            from ..panels.InfoPanel import InfoPanel
            root = self.winfo_toplevel()
            if hasattr(root, "switch_panel"):
                root.switch_panel(InfoPanel)
        except Exception as error:
            logger.error(f"Error opening InfoPanel: {error}", exc_info=True)
