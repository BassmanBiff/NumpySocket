from numpysocket import NumpyServer
import numpy as np

# Start
npSocket = NumpyServer()
npSocket.start(9999)

# Send array
frame = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
npSocket.send_array(frame)

# End
npSocket.end()
