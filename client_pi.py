# From https://stackoverflow.com/questions/30988033/
#      sending-live-video-frame-over-network-in-python-opencv

from numpysocket import NumpySocket
import cv2

npSocket = NumpySocket()
npSocket.startServer('localhost', 9999)
cv2.namedWindow('PiCamera')

# Read until video is completed
while True:
    # Receive and display frames until pressing q
    frame = npSocket.recieveNumpy()
    cv2.imshow('PiCamera', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

npSocket.endServer()
print("Closed successfully")
