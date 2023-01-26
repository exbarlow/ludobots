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
    def __init__(self,directOrGUI):
        self.directOrGUI = directOrGUI
        if self.directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        elif self.directOrGUI == "GUI":
            self.physicsClient = p.connect(p.GUI)

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
            if self.directOrGUI == "GUI":
                time.sleep(c.sleepTime)

    def Get_Fitness(self):
        self.robot.Get_Fitness()
        
        

