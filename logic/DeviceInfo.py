from socket import gethostname                                                                                                                                                 
import netifaces                                                                                                                                                               

class DeviceInfo:
    def __init__(self):
        # get the current hostname
        self.hostname = gethostname()
        # Get network interfaces
        _interfaces = netifaces.interfaces()
        # Put each in new line for better look
        self.networkInterfaces = "\n".join(_interfaces)
    
        # All IPv4 addresses from all interfaces
        # Getting ip addresses from interfaces is faster than using getbyhostname
        # because getbyhostname queries the hosts file in computer
        ip_list = []
        for iface in _interfaces:
            addrs = netifaces.ifaddresses(iface)
            if netifaces.AF_INET in addrs:
                # Gather ip addresses next to it's interface in an array
                for addr_info in addrs[netifaces.AF_INET]:
                    ip_list.append(f"{iface}: {addr_info['addr']}")
    
        # Concat the string array having new line between them so they will look like stacked
        self.ipAddress = "\n".join(ip_list)

