from tkinter import Frame

from ..components.Buttons import DeviceInfoButton, EchoTestButton, RetrieveTimeButton

class MainButtonSetPanel(Frame):
    def __init__(self, root):
        super().__init__(root, bg="lightblue", padx=10, pady=10)
        DeviceInfoButton(self).pack()
        EchoTestButton(self).pack()
        RetrieveTimeButton(self).pack()