#!/usr/bin/env python3
import socket
import sys
import pickle
import struct
import threading
from logger import get_logger

logger = get_logger("ChatClient")

# Some utilities (assumed to be used by both server and client)
def send(channel, *args):
    buffer = pickle.dumps(args)
    value = socket.htonl(len(buffer))
    size = struct.pack("L", value)
    channel.send(size)
    channel.send(buffer)

def receive(channel):
    size_data = channel.recv(struct.calcsize("L"))
    try:
        size = socket.ntohl(struct.unpack("L", size_data)[0])
    except struct.error as e:
        return ''
    buf = b""
    while len(buf) < size:
        buf += channel.recv(size - len(buf))
    return pickle.loads(buf)[0]

class ChatClient:
    """A command line chat client using a separate input thread."""
    def __init__(self, name, port, host):
        self.name = name
        self.connected = False
        self.host = host
        self.port = port
        # Initial prompt
        self.prompt = '[' + '@'.join((name, socket.gethostname().split('.')[0])) + ']> '
        # Connect to server at port
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, self.port))
            logger.info("Now connected to chat server @ port %s", self.port)
            self.connected = True
            # Send my name...
            send(self.sock, 'NAME: ' + self.name)
            data = receive(self.sock)
            # Contains client address, set it
            addr = data.split('CLIENT: ')[1]
            self.prompt = '[' + '@'.join((self.name, addr)) + ']> '
        except socket.error as e:
            logger.error("Failed to connect to chat server @ port %s: %s", self.port, e)
            sys.exit(1)

    def run(self):
        """Chat client main loop using a separate input thread."""
        def input_thread():
            # This thread handles user input from the console.
            while self.connected:
                line = sys.stdin.readline().strip()
                if line:
                    send(self.sock, line)

        # Start the input thread
        t = threading.Thread(target=input_thread, daemon=True)
        t.start()

        try:
            # Main thread: receive messages from the server.
            while self.connected:
                data = receive(self.sock)
                if not data:
                    logger.info("Client shutting down.")
                    self.connected = False
                    break
                else:
                    # Log received messages
                    logger.info("%s", data)
                    # Optionally, reprint the prompt:
                    sys.stdout.write(self.prompt)
                    sys.stdout.flush()
        except KeyboardInterrupt:
            logger.info("Client interrupted.")
        finally:
            self.sock.close()