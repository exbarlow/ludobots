
gravity = (0,0,-9.8)
timeSteps = 1000
sleepTime = 1/10000
maxForce = 250

motorJointRange = 1
numSensorNeurons = 7
numMotorNeurons = 6
## dictionary of hidden layer neurons, key is layer number, value is number of neurons in that layer
# hiddenNeurons = {0:8,1:4,2:2}
hiddenNeurons = {0:6}
mutationRate = 0.5
mutationPower = 2.5
cullSize = 5

dataPath = "data/"
savedPath = "saved_searches/"

numberOfGenerations = 30
populationSize = 30
