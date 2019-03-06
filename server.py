from numpysocket import NumpyServer
import numpy as np

npSocket = NumpyServer()
npSocket.start(9999)

frame = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
npSocket.send_array(frame)

# When everything done, release the video capture object
npSocket.end()
