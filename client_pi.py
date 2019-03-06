# From https://stackoverflow.com/questions/30988033/
#      sending-live-video-frame-over-network-in-python-opencv

from numpysocket import NumpyClient
import cv2

host_ip = '172.16.16.117'
npSocket = NumpyClient()
npSocket.start(host_ip, 9999)
cv2.namedWindow('PiCamera')

# Read until video is completed
while True:
    # Receive and display frames until pressing q
    frame = npSocket.recv_array()
    cv2.imshow('PiCamera', cv2.resize(frame << 6, None, fy=0.4, fx=0.4))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

npSocket.end()
print("Closed successfully")
