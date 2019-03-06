from numpysocket import NumpySocket

npSocket = NumpySocket()
npSocket.startClient(9999)

# Read an array
frame = npSocket.recieveNumpy()
print("Received {}, shape {}, type {}".format(
    type(frame), frame.shape, frame.dtype))

npSocket.endServer()
print("Closing")
