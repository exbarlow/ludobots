from sensor import SENSOR
from motor import MOTOR
import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import constants as c

class ROBOT:
    def __init__(self,solutionID,nndfName = ""):
        self.robotId = p.loadURDF("body.urdf")
        self.solutionID = solutionID
        self.fitness = 0
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        if nndfName == "":
            self.nn = NEURAL_NETWORK(f"brain/{self.solutionID}.nndf")
            os.system(f"rm brain/{self.solutionID}.nndf")
        else:
            self.nn = NEURAL_NETWORK(nndfName)

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
            self.motors[str(jointName)] = MOTOR(jointName)

    def Set_Fitness(self,fitness):
        self.fitness =fitness


    def Act(self):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)*c.motorJointRange
                self.motors[f"b'{jointName}'"].Set_Value(desiredAngle,self.robotId)
    
    def Save_Values(self):
        for sensor in self.sensors.values():
            sensor.Save_Values()

    def Think(self):
        self.nn.Update()
        # self.nn.Print()

    def Get_Fitness(self):
        # basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        # basePosition = basePositionAndOrientation[0]
        # yCoordinateOfLinkZero = basePosition[1]

        with open(f"tmp{self.solutionID}.txt","w") as f:
            f.write(str(self.fitness))
        os.system(f"mv tmp{self.solutionID}.txt fitness/{self.solutionID}.txt")

        # print("")
        # print(xCoordinateOfLinkZero)
        

   






