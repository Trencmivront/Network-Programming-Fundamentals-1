#!/usr/bin/env python3
# Python Network Programming Cookbook -- Chapter - 2
# This program is optimized for Python 2.7 but has been updated for Python 3.
import select
import socket
import threading
import pickle
import os
from datetime import date
from time import ctime
import struct
import logic.Settings as sett
from logger import get_logger

logger = get_logger("ChatServer")

# Same logic from logger.py
# They won't change, so it is okay to put them in python cache bs
# Root folder of project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Chats are located right below the root folder
CHAT_DIR = os.path.join(BASE_DIR, "chats")


# Ensure the chats directory exists
os.makedirs(CHAT_DIR, exist_ok=True)

# Some utilities
def send(channel, *args):
    """Send a message to given channel with size header."""
    try:
        buffer = pickle.dumps(args)
        value = socket.htonl(len(buffer))
        size = struct.pack("L", value)
        channel.sendall(size)
        channel.sendall(buffer)
        logger.debug("Sent buffer: %s", buffer)
    except Exception as e:
        logger.error("Send error: %s", e)

def receive(channel):
    """Expect a message from given channel. If no message found, return an empty string."""
    try:
        header_size = struct.calcsize("L")
        size_data = b""
        while len(size_data) < header_size:
            chunk = channel.recv(header_size - len(size_data))
            if not chunk:
                return ''
            size_data += chunk
        size = socket.ntohl(struct.unpack("L", size_data)[0])
        buf = b""
        while len(buf) < size:
            chunk = channel.recv(size - len(buf))
            if not chunk:
                return ''
            buf += chunk
        return pickle.loads(buf)[0]
    except Exception:
        return ''

class ChatServer:
    """An example chat server using select."""
    def __init__(self):
        self.host = sett.chatServerHostname
        self.port = sett.chatServerPort
        self.backlog = sett.chatServerBacklog
        
        self.clients = 0
        self.clientmap = {}
        self.outputs = []  # list of output sockets
        self.action = None
        self.running = False
        self.writer = None # initialized at run() function

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Enable re-using socket address
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Creating server
        logger.info("Setting the server")
        self.server.bind((self.host, self.port))
        logger.info("Server listening to port: %s ...", self.port)
        self.server.listen(self.backlog)

    def on_receive(self, action=None):
        """Set an action to run when a message is received or client connects."""
        if action is not None:
            self.action = action

    def message(self, text: str):
        """Broadcasts a message from server to all connected clients."""
        if not text:
            return
        msg = f"\n#[{ctime()}][Server]>>{text}"
        # write message into a file
        self.chat_write(msg)
        for output in list(self.outputs):
            send(output, msg)
        return msg

    def get_client_name(self, client):
        """Return the name of the client."""
        info = self.clientmap.get(client)
        if not info:
            return "unknown"
        host, name = info[0][0], info[1]
        return '@'.join((name, host))

    def chat_write(self, text : str):
        """Writes the sent and received chat messages into a file.
        
        The file name will be the date of which messages are written. dd/mm/yyyy
        """
        # retrieve the file writer if created
        if self.writer:
            # add a new line after each text
            # I don't add them new line since each message already has them
            self.writer.write(text)


    def close(self):
        logger.info("Shutting down server...")
        self.running = False
        # Close existing client sockets
        for output in list(self.outputs):
            try:
                output.close()
            except Exception:
                pass
        self.outputs.clear()
        self.clientmap.clear()
        try:
            # close leaks
            self.server.close()
            self.writer.close()
        except Exception:
            pass

    def start(self):
        """Starts the receive loop in a background daemon thread."""
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()
        return thread

    def run(self):
        inputs = [self.server]
        self.outputs = []
        self.running = True
        # Create a file writer which will write chats to file named date of current day.
        # it will only support append operation
        self.writer = open(os.path.join(CHAT_DIR , str(date.today()) + ".txt"), "a")
        while self.running:
            try:
                # Use a timeout (0.5s) and do not poll self.outputs for writeable to prevent 100% CPU spin
                readable, _, _ = select.select(inputs, [], [], 0.5)
            except (select.error, OSError):
                break

            for sock in readable:
                if sock == self.server:
                    # handle the server socket: new connection
                    try:
                        client, address = self.server.accept()
                    except Exception:
                        continue
                    logger.info("Chat server: got connection %s from %s", client.fileno(), address)
                    
                    raw_data = receive(client)
                    if not raw_data or 'NAME: ' not in raw_data:
                        client.close()
                        continue

                    cname = raw_data.split('NAME: ')[1].strip()
                    self.clients += 1
                    send(client, 'CLIENT: ' + str(address[0]))
                    inputs.append(client)
                    self.clientmap[client] = (address, cname)

                    client_full_name = self.get_client_name(client)
                    join_notice = f"Connected: New client ({self.clients}) from {client_full_name}"
                    msg = f"\n({join_notice})"
                    for output in list(self.outputs):
                        send(output, msg)
                    self.outputs.append(client)

                    if self.action is not None:
                        self.action(f"[{join_notice}]")
                else:
                    # handle client sockets: incoming messages
                    try:
                        data = receive(sock)
                        if data:
                            client_name = self.get_client_name(sock)
                            # Broadcast the message to all other clients
                            msg = "\n#[{}]>>{}".format(client_name, data)
                            for output in list(self.outputs):
                                if output != sock:
                                    send(output, msg)
                            
                            # Notify server UI
                            if self.action is not None:
                                self.action(f"{client_name}: {data}")
                        else:
                            # Client disconnected
                            logger.info("Chat server: %s hung up", sock.fileno())
                            self.clients -= 1
                            client_name = self.get_client_name(sock)
                            if sock in inputs:
                                inputs.remove(sock)
                            if sock in self.outputs:
                                self.outputs.remove(sock)
                            self.clientmap.pop(sock, None)
                            sock.close()

                            # Inform others of client departure
                            depart_notice = f"Now hung up: Client {client_name}"
                            msg = f"\n({depart_notice})"
                            for output in list(self.outputs):
                                send(output, msg)

                            if self.action is not None:
                                self.action(f"[{depart_notice}]")
                    except socket.error as e:
                        # Remove socket on error
                        if sock in inputs:
                            inputs.remove(sock)
                        if sock in self.outputs:
                            self.outputs.remove(sock)
                        self.clientmap.pop(sock, None)
                        try:
                            sock.close()
                        except Exception:
                            pass
                        logger.error("Socket error: %s", e)