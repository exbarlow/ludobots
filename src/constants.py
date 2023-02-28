#TODO: add comments

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

numberOfGenerations = 50
populationSize = 20

# relating to random snake generation -- minLinks should always be >= 2 !! WILL BREAK IF SET TO 1
minLinks = 2
maxLinks = 8

addLinkChance = 0.05
removeLinkChance = 0.05
flipSensorLinkChance = 0.02
newLinkSensorChance = 0.5

minSensorProportion = 0.3
maxSensorProportion = 0.7

minLinkSize = 0.25
maxLinkSize = 2

faces = {0: (1,0,0), 1: (-1,0,0), 2: (0,1,0), 3: (0,-1,0), 4: (0,0,1), 5: (0,0,-1)}
inverseFaces = {0:1,1:0,2:3,3:2,4:5,5:4}
faceToPossibleAxes = {0: (1,2), 1: (1,2), 2: (0,2), 3: (0,2), 4: (0,1), 5: (0,1)}
axesToString = {0: "1 0 0", 1: "0 1 0", 2: "0 0 1"}