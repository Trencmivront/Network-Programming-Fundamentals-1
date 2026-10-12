from tkinter import Label, Toplevel
from ..panels.DeviceInfoPanel import DeviceInfoPanel

class InfoWindow(Toplevel):
    def __init__(self, root):
        super().__init__(master=root)
        self.title="Information"
        self.transient=root

        Label(self, text="Device Information").pack(padx=20, pady=10)
        DeviceInfoPanel(self).pack(fill="both")

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.wait_visibility()  # Wait until the dialog appears
        self.grab_set()         # Block interaction with the main window