from numpysocket import NumpyClient

# Start
npSocket = NumpyClient()
npSocket.start('localhost', 9999)

# Read array
frame = npSocket.recv_array()
print("Received {}, shape {}, type {}".format(
    type(frame), frame.shape, frame.dtype))

# End
npSocket.end()
