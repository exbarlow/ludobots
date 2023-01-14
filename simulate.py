import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy as np

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


for i in range(1000):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    time.sleep(1/200)

np.save("data/backLegSensorValues.npy",backLegSensorValues)
print(backLegSensorValues)

p.disconnect()

