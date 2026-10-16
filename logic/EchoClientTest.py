import socket
from logger import get_logger

logger = get_logger("EchoClientTest")

# Documentation is made by me btw

class EchoClientTest():
    """ A simple echo client test """

    # values are taken manually, not from settings file
    def __init__(self, host, port):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the server
        server_address = (host, port)
        logger.info("Connecting to %s port %s" % server_address)
        self.sock.connect(server_address)

    def send_message(self, message, on_data, isThreadRunning):
        """Send message to connected server.
        
        Prefer using threads as this function may block your main flow.
        """
        # Send data
        try:
            # Send data
            logger.info("Sending %s" % message)
            self.sock.sendall(message.encode('utf-8'))
            # Look for the response
            amount_received = 0
            amount_expected = len(message)
            while (amount_received < amount_expected) and isThreadRunning:
                data = self.sock.recv(16)
                amount_received += len(data)
                on_data(data)
                logger.info("Received: %s" % data)
        except socket.error as e:
            logger.error("Socket error: %s" %str(e))
        except Exception as e:
            logger.error("Other exception: %s" %str(e))
        finally:
            logger.info("Closing connection to the server")
        self.sock.close()

    def close_connection(self):
        """If you won't use send_message, connection will kept open. So I wrote another method to close it manually. 
        
        If you need to reconnect, reinitialize the object.
        """
        logger.info("Closing connection to the server")
        self.sock.close()