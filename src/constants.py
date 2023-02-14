
gravity = (0,0,-9.8)
timeSteps = 1000
sleepTime = 1/1000
maxForce = 250

motorJointRange = 0.4

# dictionary of hidden layer neurons, key is layer number, value is number of neurons in that layer
hiddenNeurons = {0:6}
# controls the change of mutation
mutationRate = 0.5
# controls the magnitude of mutation
mutationPower = 2.5
# the number of top individuals selected to be the parents of the next generation is 1//cullSize
cullSize = 5

dataPath = "data/"
savedPath = "saved_searches/"
tempfilePath = "src/tempfiles/"

numberOfGenerations = 1
populationSize = 1

# relating to random snake generation -- minLinks should always be >= 2 !! WILL BREAK IF SET TO 1
minLinks = 2
maxLinks = 10

minSensorProportion = 0.3
maxSensorProportion = 0.7

minLinkSize = 0.25
maxLinkSize = 2
