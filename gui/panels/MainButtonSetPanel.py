from tkinter import Frame

# Set of buttons all in one file - class so I won't need to import them seperately.
from ..components.MenuButtons import (
    DeviceInfoButton,
    EchoTestButton,
    RetrieveTimeButton,
    ChatButton,
    SettingsButton,
)


class MainButtonSetPanel(Frame):
    def __init__(self, root):
        super().__init__(root, bg="lightblue", padx=10, pady=10)
        DeviceInfoButton(self).pack(pady=4)
        EchoTestButton(self).pack(pady=4)
        RetrieveTimeButton(self).pack(pady=4)
        ChatButton(self).pack(pady=4)
        SettingsButton(self).pack(pady=4)