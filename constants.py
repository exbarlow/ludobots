import math

gravity = (0,0,-9.8)
timeSteps = 1000
sleepTime = 1/10000
maxForce = 250

motorJointRange = 1
numSensorNeurons = 7
numMotorNeurons = 6
## dictionary of hidden layer neurons, key is layer number, value is number of neurons in that layer
hiddenNeurons = {}

dataPath = "data/"
savedPath = "saved_searches/"

numberOfGenerations = 1
populationSize = 1
