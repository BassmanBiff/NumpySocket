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
        # print("Received length: ", length)
        image_buffer = b''
        received = 0
        while received < length:
            image_buffer += self.recv(6291456)
            new_received = len(image_buffer)
            # print("Received total {}...".format(new_received))
            if new_received != received:
                received = new_received
            else:
                break
        return np.load(BytesIO(image_buffer))['frame']


class NumpyServer(NumpySocket):
    def __init__(self):
        self.buffer = BytesIO()

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
            raise TypeError("send_array requires a valid ndarray.")
        buffer = self.buffer
        np.savez_compressed(buffer, frame=image)
        self.client.send(int.to_bytes(buffer.tell(), 4, 'big'))
        # print("Sent length: ", f.tell())
        buffer.seek(0)
        self.client.sendfile(f)
        # print("Sent file.")
        buffer.seek(0)
        buffer.truncate()
        return True
