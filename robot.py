from sensor import SENSOR
from motor import MOTOR
import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
class ROBOT:
    def __init__(self):
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.nn = NEURAL_NETWORK("brain.nndf")


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

    def Act(self,t):
        for motor in self.motors.values():
            motor.Set_Value(t,self.robotId)
    
    def Save_Values(self):
        for sensor in self.sensors.values():
            sensor.Save_Values()
        
        for motor in self.motors.values():
            motor.Save_Values()

    def Think(self):
        self.nn.Print()
        

   






