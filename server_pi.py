from NumpyServer import NumpyServer
from picamera import PiCamera
from picamera.array import PiBayerArray

npSocket = NumpyServer()
npSocket.start(9999)

# Read until video is completed
with PiCamera(format='jpeg', bayer=True) as cam:
    with PiBayerArray(cam, outpit_dims=2) as stream:
        success = True
        while success:
            success = npSocket.send(stream.array)

# When everything done, release the video capture object
npSocket.end()
print("Closed successfully")
