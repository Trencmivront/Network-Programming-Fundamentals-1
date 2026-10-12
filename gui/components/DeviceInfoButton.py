from tkinter import Button
from ..frames.InfoWindow import InfoWindow

# Set of predefined classes for main menu buttons
class DeviceInfoButton(Button):
    """A button that opens a modal InfoWindow dialog when clicked, to display device information.

    :param root: Container frame for the button.
    """
    def __init__(self, master):
            super().__init__(master, text="Device Info", width=20)
            self.config(command=self.on_click)
    
    def on_click(self):
        try:
            InfoWindow(self)
        except Exception as error:
            print(error)
