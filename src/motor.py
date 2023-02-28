import numpy as np
import src.constants as c
import src.pyrosim.pyrosim as pyrosim
import pybullet as p

#TODO: add docstrings
#TODO: add comments
#TODO: add assertions?
class MOTOR:
    def __init__(self,jointName) -> None:
        self.jointName = jointName

    def Set_Value(self,desiredAngle,robotId):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex= robotId,
            jointName = self.jointName,
            controlMode= p.POSITION_CONTROL,
            targetPosition= desiredAngle,
            maxForce= c.maxForce
        )


