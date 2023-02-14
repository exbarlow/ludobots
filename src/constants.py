
gravity = (0,0,-9.8)
timeSteps = 1000
sleepTime = 1/1000
maxForce = 250

motorJointRange = 1

# dictionary of hidden layer neurons, key is layer number, value is number of neurons in that layer
hiddenNeurons = {0:6}
mutationRate = 0.5
mutationPower = 2.5
cullSize = 5

dataPath = "data/"
savedPath = "saved_searches/"
tempfilePath = "src/tempfiles/"

numberOfGenerations = 20
populationSize = 3

# relating to random snake generation -- minLinks should always be >= 2
minLinks = 2
maxLinks = 10
sensorProportion = 0.3
minLinkSize = 0.25
maxLinkSize = 2
