#!/usr/bin/env python3
# Python Network Programming Cookbook -- Chapter - 2
# This program is optimized for Python 2.7 but has been updated for Python 3.
import select
import socket
import sys
import signal
import pickle
import struct
import logic.Settings as sett
from logger import get_logger

logger = get_logger("ChatServer")

SERVER_HOST = sett.chatServerHostname
CHAT_SERVER_NAME = 'server'

# Some utilities
def send(channel, *args):
    buffer = pickle.dumps(args)
    value = socket.htonl(len(buffer))
    size = struct.pack("L", value)
    channel.send(size)
    channel.send(buffer)
    logger.debug("Sent buffer: %s", buffer)

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

class ChatServer:
    """An example chat server using select."""
    def __init__(self, host=None, port=None, backlog=None):
        self.host = host if host is not None else sett.chatServerHostname
        self.port = port if port is not None else sett.chatServerPort
        self.backlog = backlog if backlog is not None else sett.chatServerBacklog
        
        self.clients = 0
        self.clientmap = {}
        self.outputs = []  # list of output sockets
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Enable re-using socket address
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        logger.info("Server listening to port: %s ...", self.port)
        self.server.listen(self.backlog)
        # Catch keyboard interrupts
        signal.signal(signal.SIGINT, self.sighandler)

    def sighandler(self, signum, frame):
        """Clean up client outputs."""
        logger.info("Shutting down server...")
        # Close existing client sockets
        for output in self.outputs:
            output.close()
        self.server.close()
        sys.exit(0)

    def get_client_name(self, client):
        """Return the name of the client."""
        info = self.clientmap[client]
        host, name = info[0][0], info[1]
        return '@'.join((name, host))

    def run(self):
        inputs = [self.server]  # Removed sys.stdin so that the server doesn't exit immediately.
        self.outputs = []
        running = True
        while running:
            try:
                readable, writeable, exceptional = select.select(inputs, self.outputs, [])
            except select.error as e:
                break

            for sock in readable:
                if sock == self.server:
                    # handle the server socket: new connection
                    client, address = self.server.accept()
                    logger.info("Chat server: got connection %s from %s", client.fileno(), address)
                    # Read the login name
                    cname = receive(client).split('NAME: ')[1]
                    # Compute client name and send back
                    self.clients += 1
                    send(client, 'CLIENT: ' + str(address[0]))
                    inputs.append(client)
                    self.clientmap[client] = (address, cname)
                    # Send joining information to other clients
                    msg = "\n(Connected: New client ({}) from {})".format(self.clients, self.get_client_name(client))
                    for output in self.outputs:
                        send(output, msg)
                    self.outputs.append(client)
                else:
                    # handle client sockets: incoming messages
                    try:
                        data = receive(sock)
                        if data:
                            # Broadcast the message to all other clients
                            msg = "\n#[{}]>>{}".format(self.get_client_name(sock), data)
                            for output in self.outputs:
                                if output != sock:
                                    send(output, msg)
                        else:
                            # Client disconnected
                            logger.info("Chat server: %s hung up", sock.fileno())
                            self.clients -= 1
                            sock.close()
                            inputs.remove(sock)
                            if sock in self.outputs:
                                self.outputs.remove(sock)
                            # Inform others of client departure
                            msg = "\n(Now hung up: Client from {})".format(self.get_client_name(sock))
                            for output in self.outputs:
                                send(output, msg)
                    except socket.error as e:
                        # Remove socket on error
                        if sock in inputs:
                            inputs.remove(sock)
                        if sock in self.outputs:
                            self.outputs.remove(sock)
                        sock.close()
                        logger.error("Socket error: %s", e)