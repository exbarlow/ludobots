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
        

    def __del__(self):
        p.disconnect()
    
    def Run(self):

        targetAngles = np.linspace(0,2*math.pi,c.timeSteps)

        targetAngles_bl = [c.amplitude_bl * np.sin(c.frequency_bl * i + c.phaseOffset_bl) for i in targetAngles]
        targetAngles_fl = [c.amplitude_fl * np.sin(c.frequency_fl * i + c.phaseOffset_fl) for i in targetAngles]

        for i in range(c.timeSteps):
            p.stepSimulation()
            self.robot.Sense(i)

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

