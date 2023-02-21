from src.sensor import SENSOR
from src.motor import MOTOR
import pybullet as p
import src.pyrosim.pyrosim as pyrosim
from src.pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import src.constants as c

class ROBOT:
    def __init__(self,solutionID,savedName = ""):
        self.solutionID = solutionID
        self.fitness = 0
        if savedName == "":
            self.nn = NEURAL_NETWORK(f"{c.tempfilePath}brain/{self.solutionID}.nndf")
            self.robotId = p.loadURDF(f"{c.tempfilePath}body/{self.solutionID}.urdf")
            os.system(f"rm {c.tempfilePath}brain/{self.solutionID}.nndf")
            os.system(f"rm {c.tempfilePath}body/{self.solutionID}.urdf")
        else:
            self.nn = NEURAL_NETWORK(f"{c.savedPath}brain/{savedName}.nndf")
            self.robotId = p.loadURDF(f"{c.savedPath}body/{savedName}.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
            

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self,t):
        for sensor in self.sensors.values():
            sensor.Get_Value(t)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Set_Fitness(self,fitness):
        self.fitness =fitness


    def Act(self):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)*c.motorJointRange
                self.motors['{}'.format(jointName).encode()].Set_Value(desiredAngle,self.robotId)
    
    def Save_Values(self):
        for sensor in self.sensors.values():
            sensor.Save_Values()

    def Think(self):
        self.nn.Update()

    def Get_Fitness(self):

        with open(f"{c.tempfilePath}tmp{self.solutionID}.txt","w") as f:
            f.write(str(self.fitness))
        os.system(f"mv {c.tempfilePath}tmp{self.solutionID}.txt {c.tempfilePath}fitness/{self.solutionID}.txt")
        

   






