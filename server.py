from numpysocket import NumpySocket
import numpy as np

host_ip = '172.16.16.117'  # change me
npSocket = NumpySocket()
npSocket.startServer(host_ip, 9999)

frame = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
npSocket.sendNumpy(frame)

# When everything done, release the video capture object
npSocket.endServer()
