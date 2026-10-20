#!/usr/bin/env python3
import socket
import sys
import pickle
import struct
import threading
import os
from datetime import date
from time import ctime
from logger import get_logger

logger = get_logger("ChatClient")

# Same logic from logger.py
# They won't change, so it is okay to put them in python cache bs
# Root folder of project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Chats are located right below the root folder
CHAT_DIR = os.path.join(BASE_DIR, "chats")


# Ensure the chats directory exists
os.makedirs(CHAT_DIR, exist_ok=True)

# Some utilities (assumed to be used by both server and client)
# I wil keep these functions as are
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

        self.action = None # Set action before so no error comes out
        self.writer = None # initialized at run() function
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
            raise

    def chat_write(self, text : str):
        """Writes the sent and received chat messages into a file.
        
        The file name will be the date of which messages are written. dd/mm/yyyy
        """
        # retrieve the file writer if created
        if self.writer:
            # add a new line after each text
            # I don't add them new line since each message already has them
            self.writer.write(text)
            self.writer.flush()

    def message(self, text: str):
        """Sends a string message to the server."""
        if not text:
            return
        msg = f"\n#[{ctime()}][{self.name}]>>{text}"
        self.chat_write(msg)
        if self.connected:
            try:
                send(self.sock, text)
            except Exception as e:
                logger.error("Failed to send message: %s", e)

    def start(self):
        """Starts the receive loop in a background daemon thread."""
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()
        return thread

    def run(self):
        """Chat client main loop: receives messages from the server."""
        # Create a file writer which will write chats to file named date of current day.
        # it will only support append operation
        self.writer = open(os.path.join(CHAT_DIR , str(date.today()) + ".txt"), "a")
        try:
            while self.connected:
                data = receive(self.sock)
                if not data:
                    logger.info("Client shutting down.")
                    self.connected = False
                    break
                else:
                    self.chat_write(data)
                    if self.action is not None:
                        self.action(data)
                    logger.info("Received data: %s", data)
        except Exception as e:
            if self.connected:
                logger.error("Client receive error: %s", e)
        finally:
            self.connected = False
            try:
                self.sock.close()
            except Exception:
                pass
            try:
                if self.writer:
                    self.writer.close()
            except Exception:
                pass

    def close(self):
        """Closes the client connection and releases the socket."""
        self.connected = False
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        try:
            self.sock.close()
        except Exception:
            pass
        try:
            if self.writer:
                self.writer.close()
        except Exception:
            pass

    def on_receive(self, action=None):
        """Set an action to run when a message is received."""
        if action is not None:
            self.action = action