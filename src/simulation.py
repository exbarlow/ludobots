from src.world import WORLD
from src.robot import ROBOT
import pybullet as p
import pybullet_data
import src.constants as c
import time
import os


class SIMULATION:
    def __init__(self,directOrGUI:str,solutionID:int,savedName:str=""):
        #TODO: add type annotation
        #TODO: add docstring
        #TODO: add comments
        self.directOrGUI = directOrGUI
        if self.directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        elif self.directOrGUI == "GUI":
            self.physicsClient = p.connect(p.GUI)
        p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.world = WORLD()
        self.robot = ROBOT(solutionID,savedName)
        self.savedName = savedName
        p.setGravity(*c.gravity)
        

    def __del__(self):
        p.disconnect()
    
    def Run(self):
        """
        Runs the simulation.

        @param `savedName`: The name of the file to simulate. This should only include the saved name, not the folder structure. This is only used when calling this function from the `scripts/viewSaved.py` script.

        @return: `None`
        """

        # if the fitnessFile and brainFile exist add text to the screen with the file and the fitness
        fitnessFile = f"{c.savedPath}fitness/{self.robot.solutionID}.txt"
        brainFile = f"{c.savedPath}brain/{self.robot.solutionID}.nndf"
        bodyFile = f"{c.savedPath}body/{self.robot.solutionID}.urdf"
        if os.path.exists(fitnessFile) and os.path.exists(brainFile) and os.path.exists(bodyFile):
            # read the fitness into a variable
            with open(fitnessFile,"r") as f:
                fitness = f.read()

            # add the text to the screen
            p.addUserDebugText(f"Solution: {self.robot.solutionID}", [-5, -2, 2], textColorRGB=[1, 0, 0], textSize=1.5)
            p.addUserDebugText(f"Fitness: {fitness}", [-5, -2, 0.5], textColorRGB=[1, 0, 0], textSize=1.5)
        elif self.savedName != "":
            # if the files don't exist & we are given a self.savedName, it means we are calling this function from the viewSavedSearches.py script with a provided fileName
            fitnessFile = f"{c.savedPath}fitness/{self.savedName}.txt"
            brainFile = f"{c.savedPath}brain/{self.savedName}.nndf"

            # read the fitness into a variable
            with open(fitnessFile,"r") as f:
                fitness = f.read()
            
            # add the text to the screen
            p.addUserDebugText(f"FileName: {self.savedName} ", [-5, -2, 2], textColorRGB=[1, 0, 0], textSize=1.5)
            p.addUserDebugText(f"Fitness: {fitness}", [-5, -2, 0.5], textColorRGB=[1, 0, 0], textSize=1.5)

        # for each time step, sense the world, think, act, and keep track of fitness
        for i in range(c.timeSteps):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act()
                
            if self.directOrGUI == "GUI":
                time.sleep(c.sleepTime)

        self.robot.Set_Fitness(p.getAABB(self.robot.robotId)[1][1])

    def Get_Fitness(self):
        #TODO add docstring
        self.robot.Get_Fitness()
        
        

