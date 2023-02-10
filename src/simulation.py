from world import WORLD
from robot import ROBOT
import pybullet as p
import pybullet_data
import constants as c
import time


class SIMULATION:
    def __init__(self,directOrGUI,solutionID,nndfName=""):
        self.directOrGUI = directOrGUI
        if self.directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        elif self.directOrGUI == "GUI":
            self.physicsClient = p.connect(p.GUI)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.world = WORLD()
        self.robot = ROBOT(solutionID,nndfName)
        p.setGravity(*c.gravity)
        

    def __del__(self):
        p.disconnect()
    
    def Run(self,fileName=""):

        lastBounce = None
        largestBounce = 0

        if fileName != "":
            nameId = p.addUserDebugText(f"File: {fileName}", [-5, -2, 2], textColorRGB=[1, 0, 0], textSize=1.5)
        for i in range(c.timeSteps):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act()

            if len(p.getContactPoints(self.robot.robotId,self.world.planeId)) > 0:
                if lastBounce == None:
                    lastBounce = i
                else:
                    bounce = i - lastBounce
                    largestBounce = max(bounce,largestBounce)
                
            self.robot.Set_Fitness(largestBounce)
            if self.directOrGUI == "GUI":
                time.sleep(c.sleepTime)

    def Get_Fitness(self):
        self.robot.Get_Fitness()
        
        

