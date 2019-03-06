from numpysocket import NumpyServer
import numpy as np

# Start
npSocket = NumpyServer()
npSocket.start(9999)

# Send array
frame = np.zeros((10000, 10000))
npSocket.send_array(frame)

# End
npSocket.end()
