from tkinter import Frame, Label
from logic.DeviceInfo import hostname, ipAddress, networkInterfaces

class DeviceInfoPanel(Frame):
    def __init__(self, root):
        super().__init__(root, padx=10, pady=10)

        hostFrame = Frame(self)
        Label(hostFrame,text = "Hostname: ", font=("TkDefaultFont", 18, "bold")).pack(side="left")
        Label(hostFrame, text=hostname).pack(side="left")
        hostFrame.pack()

        netIfacesFrame = Frame(self)
        Label(netIfacesFrame, text= "Network Interfaces: ", font=("TkDefaultFont", 18, "bold")).pack(side="left")
        Label(netIfacesFrame, text= networkInterfaces).pack(side="left")
        netIfacesFrame.pack()

        ipFrame = Frame(self)
        Label(ipFrame, text = "IP Address: ", font=("TkDefaultFont", 18, "bold")).pack(side="left")
        Label(ipFrame, text= ipAddress).pack(side="left")
        ipFrame.pack()


