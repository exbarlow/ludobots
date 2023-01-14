import numpy as np
import matplotlib.pyplot as mpl

backLegSensorValues = np.load("data/backLegSensorValues.npy")

mpl.plot(backLegSensorValues)
mpl.show()