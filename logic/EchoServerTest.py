import socket

from logic.Settings import echoTestHost, echoTestBacklog, echoTestDataPayload, echoTestPort, echoTestTimeout

from logger import get_logger

logger = get_logger("EchoServerTest")
# The values are taken from Settings.py file

def echo_server(on_data, is_thread_running):
    """ Echo test server """
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Enable reuse address/port
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to the port
    server_address = (echoTestHost, echoTestPort)
    logger.info("Starting up echo server on %s port %s" % server_address)
    sock.bind(server_address)
    # Listen to clients, echoTestBacklog argument specifies the max no. of queued connections
    sock.listen(echoTestBacklog)
    # restart loop after some time
    sock.settimeout(echoTestTimeout)

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
        client.settimeout(echoTestTimeout)
        try:
            data = client.recv(echoTestDataPayload)
            if data:
                logger.info("Data: %s" %data)
                client.send(data)
                logger.info("sent %s bytes back to %s" % (data, address))
                # end connection
                client.close()
                sock.shutdown(socket.SHUT_RDWR)
                on_data(data)
                break
        except client.timeout:
            logger.warning("Client timeout, restarting...")
        except Exception as error:
            logger.error("AAAAAAAAAA: %s", error)

# python 13-server-tcp.py --port=9900
