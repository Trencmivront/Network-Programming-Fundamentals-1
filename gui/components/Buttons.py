from .MenuButton import MenuButton
from ..frames.InfoWindow import InfoWindow

# Set of predefined classes for main menu buttons
class DeviceInfoButton(MenuButton):
    """A button that opens a modal InfoWindow dialog when clicked, to display device information.

    :param root: Container frame for the button.
    """
    def __init__(self, master):
        super().__init__(master, text="Device Info Button", width=20, window=InfoWindow)

class EchoTestButton(MenuButton):
    def __init__(self, master):
        super().__init__(master, text="Echo Connection Test", width=20, window=InfoWindow)

class RetrieveTimeButton(MenuButton):
    def __init__(self, master):
        super().__init__(master, text="Retrieve Current Time", width=20, window=InfoWindow)