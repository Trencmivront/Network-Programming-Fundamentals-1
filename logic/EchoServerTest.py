import socket
import logic.Settings as sett
from logger import get_logger

logger = get_logger("EchoServerTest")
# The values are taken from Settings.py file
# force the damn class retrieve new settings. f***ing python.
class EchoServerTest:
    def __init__(self):
        pass
    def echo_server(self, on_data, is_thread_running, stop_timer):
        """ Echo test server """
        # Create a TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Enable reuse address/port
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind the socket to the port
        server_address = (sett.echoServerHost, sett.echoServerPort)
        logger.info("Starting up echo server on %s port %s" % server_address)
        sock.bind(server_address)
        # Listen to clients, echoServerBacklog argument specifies the max no. of queued connections
        sock.listen(sett.echoServerBacklog)
        sock.setblocking(sett.echoServerBlocking)
        if not sett.echoServerBlocking:
            # restart loop after some time
            sock.settimeout(sett.echoTestTimeout)

        repeat = sett.echoClientPayloadCount

        while is_thread_running():
            print("Waiting to receive message from client")
            try:
                client, address = sock.accept()
            except socket.timeout:
                logger.warning("Socket timeout, restarting...")
                continue
            except Exception as error:
                logger.error("Server accept error: %s", error)
                break
            client.setblocking(sett.echoServerBlocking)
            if not sett.echoServerBlocking:
                client.settimeout(sett.echoTestTimeout)
            try:
                data = client.recv(sett.echoServerDataPayload)
                if data:
                    logger.info("Data: %s" %data)
                    client.send(data)
                    logger.info("sent %s bytes back to %s" % (data, address))
                    # end connection
                    client.close()
                    on_data(data)
                    if(repeat > 0):
                        repeat -= 1
                    if(repeat is 0):
                        # exit loop, stop server and stop the timer
                        logger.info("Payload count %i reached, closing the server.", sett.echoClientPayloadCount)
                        sock.shutdown(socket.SHUT_RDWR)
                        stop_timer()
                        break
                    # if none of them above, just continue listening
            
            except client.timeout:
                logger.warning("Client timeout, restarting...")
            except Exception as error:
                logger.error("AAAAAAAAAA: %s", error)