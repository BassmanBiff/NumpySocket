#!/usr/bin/env python

import numpy as np
import socket
from io import BytesIO

MAX_BUF = 6291456


class NumpySocket(socket.socket):
    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer = BytesIO()


class NumpyClient(NumpySocket):
    def start(self, address, port):
        self.address, self.port = address, port
        self.connect((address, port))

    def end(self):
        self.shutdown(1)
        self.close()

    def recv_array(self):
        buffer = self.buffer
        length = int.from_bytes(self.recv(4), 'big')
        if length > MAX_BUF:                # If too big for kernel, use chunks
            while buffer.tell() < length:
                chunk = self.recv(MAX_BUF)  # Doesn't actually fill the buffer?
                buffer.write(chunk)
        else:
            buffer.write(self.recv(length, socket.MSG_WAITALL))
        buffer.seek(0)
        array = np.load(buffer)['array']
        buffer.seek(0)
        buffer.truncate()
        return array


class NumpyServer(NumpySocket):
    def start(self, port):
        self.bind(('', port))
        self.listen(1)
        self.client, self.client_address = self.accept()

    def end(self):
        try:
            self.client.shutdown(1)
        except Exception:
            pass
        self.client.close()

    def send_array(self, array):
        if not isinstance(array, np.ndarray):
            raise TypeError("send_array requires a valid ndarray.")
        buffer = self.buffer
        np.savez_compressed(buffer, array=array)
        self.client.send(int.to_bytes(buffer.tell(), 4, 'big'))
        buffer.seek(0)
        sent = self.client.sendfile(buffer)
        buffer.seek(0)
        buffer.truncate()
        return sent
