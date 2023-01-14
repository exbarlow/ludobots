import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy as np
import math
import random

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

## Set up world
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")

## Prepare robot simulation
pyrosim.Prepare_To_Simulate(robotId)
backLegSensorValues = np.zeros(1000)
frontLegSensorValues = np.zeros(1000)

#!!!!!! G7 should be `robotID` not `robot`, as we were previously told to store the id in `robotId

for i in range(1000):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    pyrosim.Set_Motor_For_Joint(
        bodyIndex= robotId,
        jointName = b'Torso_BackLeg',
        controlMode= p.POSITION_CONTROL,
        targetPosition= (random.uniform(-math.pi/2,math.pi/2)),
        maxForce= 50
    )
    pyrosim.Set_Motor_For_Joint(
        bodyIndex= robotId,
        jointName = b'Torso_FrontLeg',
        controlMode= p.POSITION_CONTROL,
        targetPosition= (random.uniform(-math.pi/2,math.pi/2)),
        maxForce= 50
    )
    time.sleep(1/100)


np.save("data/backLegSensorValues.npy",backLegSensorValues)
np.save("data/frontLegSensorValues.npy",frontLegSensorValues)

p.disconnect()

