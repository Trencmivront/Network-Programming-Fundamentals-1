from tkinter import Label, Button, Toplevel

class InfoWindow:
    def __init__(self, root):
        dialog = Toplevel(root)
        dialog.title("Dialog")
        dialog.transient(root)  # Associate it with the main window

        Label(dialog, text="Device Information").pack(padx=20, pady=10)

        dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)
        dialog.wait_visibility()  # Wait until the dialog appears
        dialog.grab_set()         # Block interaction with the main window