from socket import gethostname, gethostbyname
from netifaces import interfaces

hostname = gethostname()
ipAddress = gethostbyname(hostname)
# tagging this as private. Only is a warning
_interfaces = interfaces()
networkInterfaces = " ".join(_interfaces)
