from world import WORLD
from robot import ROBOT
import pybullet as p
import pybullet_data
import constants as c
import time
import os


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
    
    def Run(self,savedName=""):
        """
        Runs the simulation.

        @savedName: The name of the file to simulate. This should only include the saved name, not the folder structure. This is only used when calling this function from the viewSavedSearches.py script.

        @return: None
        """

        # if the fitnessFile and brainFile exist add text to the screen with the file and the fitness
        fitnessFile = f"{c.savedPath}fitness/{self.robot.solutionID}.txt"
        brainFile = f"{c.savedPath}brain/{self.robot.solutionID}.nndf"
        if os.path.exists(fitnessFile) and os.path.exists(brainFile):
            # read the fitness into a variable
            with open(fitnessFile,"r") as f:
                fitness = f.read()

            # add the text to the screen
            p.addUserDebugText(f"Solution: {self.robot.solutionID}", [-5, -2, 2], textColorRGB=[1, 0, 0], textSize=1.5)
            p.addUserDebugText(f"Fitness: {fitness}", [-5, -2, 0.5], textColorRGB=[1, 0, 0], textSize=1.5)
        elif savedName != "":
            # if the files don't exist & we are given a savedName, it means we are calling this function from the viewSavedSearches.py script with a provided fileName
            fitnessFile = f"{c.savedPath}fitness/{savedName}.txt"
            brainFile = f"{c.savedPath}brain/{savedName}.nndf"

            # read the fitness into a variable
            with open(fitnessFile,"r") as f:
                fitness = f.read()
            
            # add the text to the screen
            p.addUserDebugText(f"FileName: {savedName} ", [-5, -2, 2], textColorRGB=[1, 0, 0], textSize=1.5)
            p.addUserDebugText(f"Fitness: {fitness}", [-5, -2, 0.5], textColorRGB=[1, 0, 0], textSize=1.5)

        lastBounce = None
        largestBounce = 0

        # for each time step, sense the world, think, act, and keep track of fitness
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
                    lastBounce = i
                    largestBounce = max(bounce,largestBounce)
                
            self.robot.Set_Fitness(largestBounce)
            if self.directOrGUI == "GUI":
                time.sleep(c.sleepTime)

    def Get_Fitness(self):
        self.robot.Get_Fitness()
        
        

