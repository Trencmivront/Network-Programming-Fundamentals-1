from tkinter import Label, Toplevel
from ..panels.DeviceInfoPanel import DeviceInfoPanel
from logger import get_logger

logger = get_logger("InfoWindow")
class InfoWindow(Toplevel):
    def __init__(self, root):
        super().__init__(master=root)
        self.title="Information"
        self.transient=root

        Label(self, text="Device Information", font=("TkDefaultFont", 20, "bold")).pack(padx=20, pady=10)
        DeviceInfoPanel(self).pack(fill="both")
        # Destroy the dialog if it lost focus
        # When even occour, it is passed to the function given in bind. If I write only function itself, it takes event and self arguments.
        # This gives error since destroy function only expects "self" input.
        # Using lambda, we tell that we expect an input, so we take it but never need to use it.
        self.bind("<FocusOut>", lambda event: self.destroy())

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.wait_visibility()  # Wait until the dialog appears
        self.grab_set()         # Block interaction with the main window
    def destroy(self):
        logger.info("Destroying InfoWindow")
        return super().destroy()