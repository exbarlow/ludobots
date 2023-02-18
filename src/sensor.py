import numpy as np
import src.constants as c
import src.pyrosim.pyrosim as pyrosim
import math

class SENSOR:
    def __init__(self,linkName):
        self.linkName = linkName
        self.values = np.zeros(c.timeSteps)

    def Get_Value(self,i):
        self.values[i] = math.sin(10*pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName))

    def Save_Values(self):
        np.save(c.dataPath + f"{self.linkName}_sensor_values.npy",self.values)


