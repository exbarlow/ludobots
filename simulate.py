import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy as np
import math
import random
import constants as c


physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

## Set up world
p.setGravity(*c.gravity)

planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")

## Prepare robot simulation
pyrosim.Prepare_To_Simulate(robotId)
backLegSensorValues = np.zeros(c.timeSteps)
frontLegSensorValues = np.zeros(c.timeSteps)

targetAngles = np.linspace(0,2*math.pi,c.timeSteps)

targetAngles_bl = [c.amplitude_bl * np.sin(c.frequency_bl * i + c.phaseOffset_bl) for i in targetAngles]
targetAngles_fl = [c.amplitude_fl * np.sin(c.frequency_fl * i + c.phaseOffset_fl) for i in targetAngles]

# np.save("data/targetAngles_bl.npy",targetAngles_bl)
# np.save("data/targetAngles_fl.npy",targetAngles_fl)
# exit()

#!!!!!! G7 should be `robotID` not `robot`, as we were previously told to store the id in `robotId

for i in range(c.timeSteps):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    pyrosim.Set_Motor_For_Joint(
        bodyIndex= robotId,
        jointName = b'Torso_BackLeg',
        controlMode= p.POSITION_CONTROL,
        targetPosition= targetAngles_bl[i],
        maxForce= c.maxForce
    )
    pyrosim.Set_Motor_For_Joint(
        bodyIndex= robotId,
        jointName = b'Torso_FrontLeg',
        controlMode= p.POSITION_CONTROL,
        targetPosition= targetAngles_fl[i],
        maxForce= c.maxForce
    )
    time.sleep(c.sleepTime)


np.save("data/backLegSensorValues.npy",backLegSensorValues)
np.save("data/frontLegSensorValues.npy",frontLegSensorValues)

p.disconnect()

