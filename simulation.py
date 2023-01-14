from world import WORLD
from robot import ROBOT
import pybullet as p
import pybullet_data
import constants as c
import pyrosim.pyrosim as pyrosim
import numpy as np
import time
import math

class SIMULATION:
    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.world = WORLD()
        self.robot = ROBOT()
        p.setGravity(*c.gravity)
        pyrosim.Prepare_To_Simulate(self.robot.robotId)
    
    def Run(self):

        backLegSensorValues = np.zeros(c.timeSteps)
        frontLegSensorValues = np.zeros(c.timeSteps)

        targetAngles = np.linspace(0,2*math.pi,c.timeSteps)

        targetAngles_bl = [c.amplitude_bl * np.sin(c.frequency_bl * i + c.phaseOffset_bl) for i in targetAngles]
        targetAngles_fl = [c.amplitude_fl * np.sin(c.frequency_fl * i + c.phaseOffset_fl) for i in targetAngles]

        for i in range(c.timeSteps):
            p.stepSimulation()
            backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
            frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
            pyrosim.Set_Motor_For_Joint(
                bodyIndex= self.robot.robotId,
                jointName = b'Torso_BackLeg',
                controlMode= p.POSITION_CONTROL,
                targetPosition= targetAngles_bl[i],
                maxForce= c.maxForce
            )
            pyrosim.Set_Motor_For_Joint(
                bodyIndex= self.robot.robotId,
                jointName = b'Torso_FrontLeg',
                controlMode= p.POSITION_CONTROL,
                targetPosition= targetAngles_fl[i],
                maxForce= c.maxForce
            )

            time.sleep(c.sleepTime)

        p.disconnect()
