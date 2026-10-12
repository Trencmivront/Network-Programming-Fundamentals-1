from tkinter import Frame, Label
import socket as sc

def get_interfaces():
    import netifaces
    return netifaces.interfaces()

class DeviceInfoPanel(Frame):
    hostname = sc.gethostname()
    ipAddress = sc.gethostbyname(hostname)
    interfaces = get_interfaces()
    netWorkInterfaces = ""
    for s in interfaces:
        netWorkInterfaces += s + "  "
    def __init__(self, root):
        super().__init__(root, padx=10, pady=10)

        hostFrame = Frame(self)
        Label(hostFrame,text = "Hostname: ", font=("TkDefaultFont", 18, "bold")).pack(side="left")
        Label(hostFrame, text=self.hostname).pack(side="left")
        hostFrame.pack()

        netIfacesFrame = Frame(self)
        Label(netIfacesFrame, text= "Network Interfaces: ", font=("TkDefaultFont", 18, "bold")).pack(side="left")
        Label(netIfacesFrame, text= self.netWorkInterfaces).pack(side="left")
        netIfacesFrame.pack()

        ipFrame = Frame(self)
        Label(ipFrame, text = "IP Address: ", font=("TkDefaultFont", 18, "bold")).pack(side="left")
        Label(ipFrame, text=self.ipAddress).pack(side="left")
        ipFrame.pack()


