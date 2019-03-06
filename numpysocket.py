#!/usr/bin/env python

import numpy as np
import socket
from io import BytesIO


class NumpySocket(socket.socket):
    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.address = 0
        self.port = 0


class NumpyClient(NumpySocket):
    def start(self, address, port):
        self.address = address
        self.port = port
        try:
            self.connect((self.address, self.port))
            print('Connected to {} on port {}'.format(
                self.address, self.port))
        except socket.error as e:
            print('Connection to {} on port {} failed: {}'.format(
                self.address, self.port, e))
            return

    def end(self):
        self.shutdown(1)
        self.close()

    def recv_array(self):
        length = int.from_bytes(self.recv(4), 'big')
        print("Received length: ", length)
        image_buffer = b''
        received = 0
        while received < length:
            image_buffer += self.recv(4096)
            new_received = len(image_buffer)
            print("Received total {}...".format(new_received))
            if new_received != received:
                received = new_received
            else:
                break
        return np.load(BytesIO(image_buffer))['frame']


class NumpyServer(NumpySocket):
    def start(self, port):
        self.address = ''
        self.port = port
        self.bind((self.address, self.port))
        self.listen(1)
        self.client, self.client_address = self.accept()

    def end(self):
        self.client.shutdown(1)
        self.client.close()

    def send_array(self, image):
        if not isinstance(image, np.ndarray):
            print('not a valid numpy image')
            return False
        try:
            f = BytesIO()
            np.savez_compressed(f, frame=image)
            self.sendall(int.to_bytes(f.tell(), 4, 'big'))
            print("Sent length: ", f.tell())
            f.seek(0)
            self.socket.sendfile(f)
            print("Sent file.")
        except Exception as e:
            print(e)
            return False
        return True
