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
timeSteps = 1000
backLegSensorValues = np.zeros(timeSteps)
frontLegSensorValues = np.zeros(timeSteps)

amplitude_bl = math.pi/4
frequency_bl = 5
phaseOffset_bl = 0

amplitude_fl = math.pi/4
frequency_fl = 5
phaseOffset_fl = math.pi/2

targetAngles = np.linspace(0,2*math.pi,timeSteps)

targetAngles_bl = [amplitude_bl * np.sin(frequency_bl * i + phaseOffset_bl) for i in targetAngles]
targetAngles_fl = [amplitude_fl * np.sin(frequency_fl * i + phaseOffset_fl) for i in targetAngles]

# np.save("data/targetAngles_bl.npy",targetAngles_bl)
# np.save("data/targetAngles_fl.npy",targetAngles_fl)
# exit()

#!!!!!! G7 should be `robotID` not `robot`, as we were previously told to store the id in `robotId

for i in range(timeSteps):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    pyrosim.Set_Motor_For_Joint(
        bodyIndex= robotId,
        jointName = b'Torso_BackLeg',
        controlMode= p.POSITION_CONTROL,
        targetPosition= targetAngles_bl[i],
        maxForce= 250
    )
    pyrosim.Set_Motor_For_Joint(
        bodyIndex= robotId,
        jointName = b'Torso_FrontLeg',
        controlMode= p.POSITION_CONTROL,
        targetPosition= targetAngles_fl[i],
        maxForce= 250
    )
    time.sleep(1/800)


np.save("data/backLegSensorValues.npy",backLegSensorValues)
np.save("data/frontLegSensorValues.npy",frontLegSensorValues)

p.disconnect()

