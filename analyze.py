import numpy as np
import matplotlib.pyplot as mpl

backLegSensorValues = np.load("data/backLegSensorValues.npy")
frontLegSensorValues = np.load("data/frontLegSensorValues.npy")
targetAngles_bl = np.load("data/targetAngles_bl.npy")
targetAngles_fl = np.load("data/targetAngles_fl.npy")
# mpl.plot(backLegSensorValues,linewidth=3)
# mpl.plot(frontLegSensorValues)
# mpl.legend(['Back Leg','Front Leg'])
mpl.plot(targetAngles_bl, linewidth=3)
mpl.plot(targetAngles_fl)
mpl.legend(['Back Leg','Front Leg'])
mpl.show()