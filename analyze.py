import numpy as np
import matplotlib.pyplot as mpl

backLegSensorValues = np.load("data/backLegSensorValues.npy")
frontLegSensorValues = np.load("data/frontLegSensorValues.npy")

mpl.plot(backLegSensorValues,linewidth=3)
mpl.plot(frontLegSensorValues)
mpl.legend(['Back Leg','Front Leg'])
mpl.show()