from numpysocket import NumpyClient

npSocket = NumpyClient()
npSocket.start(9999)

# Read an array
frame = npSocket.recv_array()
print("Received {}, shape {}, type {}".format(
    type(frame), frame.shape, frame.dtype))

npSocket.end()
print("Closing")
