#!/usr/bin/env python

import socket
import numpy as np
from io import BytesIO


class NumpySocket():
    def __init__(self):
        self.address = 0
        self.port = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.type = None  # client or server

    # def __del__(self):
    #     if self.type is "server":
    #         self.endServer()
    #     if self.type is "client":
    #         self.endClient()
    #     print(self.id, 'closed')

    def startClient(self, address, port):
        self.type = "client"
        self.address = address
        self.port = port
        try:
            self.socket.connect((self.address, self.port))
            print('Connected to %s on port %s' % (
                self.address, self.port))
        except socket.error as e:
            print('Connection to %s on port %s failed: %s' % (
                self.address, self.port, e))
            return

    def endClient(self):
        self.socket.shutdown(1)
        self.socket.close()

    def sendNumpy(self, image):
        if not isinstance(image, np.ndarray):
            print('not a valid numpy image')
            return False

        try:
            f = BytesIO()
            np.savez_compressed(f, frame=image)
            self.socket.sendall(int.to_bytes(f.tell(), 4, 'big'))
            f.seek(0)
            self.socket.sendfile(f)
        except Exception as e:
            print(e)
            return False

        print('image sent')
        return True

    def startServer(self, port):
        self.type = "server"
        self.address = ''
        self.port = port

        self.socket.bind((self.address, self.port))
        self.socket.listen(1)
        print('waiting for a connection...')
        self.server_connection, self.server_address = self.socket.accept()
        print('connected to ', self.server_address[0])

    def endServer(self):
        self.server_connection.shutdown(1)
        self.server_connection.close()

    def recieveNumpy(self):
        length = int.from_bytes(self.server_connection.recv(4), 'big')
        image_buffer = b''
        received = 0
        while received < length:
            image_buffer += self.server_connection.recv(4096)
            new_received = len(image_buffer)
            if new_received != received:
                received = new_received
            else:
                break
        final_image = np.load(BytesIO(image_buffer))['frame']
        print('frame received')
        return final_image
