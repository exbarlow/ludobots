import numpy as np
import constants as c
import math
import pyrosim.pyrosim as pyrosim
import pybullet as p
class MOTOR:
    def __init__(self,jointName) -> None:
        self.jointName = jointName
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        self.amplitude = c.amplitude
        self.frequency = c.frequency
        self.offset = c.phaseOffset

        if "Front" in str(self.jointName):
            self.amplitude *= 2

        self.motorValues = [self.amplitude * np.sin(self.frequency* i + self.offset) for i in np.linspace(0,2*math.pi,c.timeSteps)]

    def Set_Value(self,desiredAngle,robotId):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex= robotId,
            jointName = self.jointName,
            controlMode= p.POSITION_CONTROL,
            targetPosition= desiredAngle,
            maxForce= c.maxForce
        )

    def Save_Values(self):
        np.save(c.dataPath + f"{self.jointName}_motor_values.npy",self.motorValues)

