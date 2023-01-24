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
        self.physicsClient = p.connect(p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.world = WORLD()
        self.robot = ROBOT()
        p.setGravity(*c.gravity)
        

    def __del__(self):
        p.disconnect()
    
    def Run(self):

        for i in range(c.timeSteps):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act()

            time.sleep(c.sleepTime)

    def Get_Fitness(self):
        self.robot.Get_Fitness()
        
        

