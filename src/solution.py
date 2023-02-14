import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import constants as c
from simulation import SIMULATION
import time

class SOLUTION:
    def __init__(self,sol_id):
        #!! HUGE FUTURE ISSUE: everything gets rerandomized each generation => need to fix this!!
        self.myID = sol_id
        # randomize number of links
        self.numLinks = np.random.randint(c.minLinks,c.maxLinks)
        # fill in link names
        self.linkNames = [str(link) for link in range(self.numLinks)]
        # fill in joint names
        self.jointNames = []
        for i in range(self.numLinks-1):
            self.jointNames.append(f"{self.linkNames[i]}_{self.linkNames[i+1]}")
        # randomize link lengths
        self.linksToLengths = {}
        for link in self.linkNames:
            self.linksToLengths[link] = np.random.uniform(c.minLinkSize,c.maxLinkSize,(3,))

        self.sensorLinks = set()
        self.Get_Sensor_Links()

        self.weights = dict()
        # create random weights dependent on number of neurons
        self.Create_Weights()
        

    def __lt__(self,other):
        return self.fitness < other.fitness

    def Get_Sensor_Links(self):
        """
        Randomly choose which links will have sensors

        @return: None
        """
        # get the proportion of links that will have sensors
        sensorProportion = np.random.uniform(c.minSensorProportion,c.maxSensorProportion)
        # get the number of links that will have sensors -> will be at least 1
        numSensorLinks = max(int(sensorProportion * self.numLinks),1)
        # choose which links will have sensors
        indices = np.random.choice(self.numLinks,numSensorLinks,replace=False)
        # add the names of the links that will have sensors to the set of sensor links
        for index in indices:
            self.sensorLinks.add(self.linkNames[index])
        #! DEBUG
        print("numLinks: ",self.numLinks)
        print("sensorProportion: ",sensorProportion)
        print("numSensorLinks: ",numSensorLinks)
        print("indices: ",indices)
        print("sensorLinks: ",self.sensorLinks)
        


    def Create_Weights(self):
        numLayers = len(c.hiddenNeurons)
        numSensorNeurons = len(self.sensorLinks)
        numMotorNeurons = self.numLinks - 1
        # If there is no hidden layer, just create weights from sensors to motors
        if numLayers == 0:
            self.weights[0] = np.random.rand(numSensorNeurons,numMotorNeurons) * 2 - 1
        # If there is only one hidden layer, create weights from sensors to first hidden layer and from first hidden layer to motors
        elif numLayers == 1:
            self.weights[0] = np.random.rand(numSensorNeurons,c.hiddenNeurons[0]) * 2 - 1
            self.weights[1] = np.random.rand(c.hiddenNeurons[0],numMotorNeurons) * 2 - 1
        else:
        # Else, we will create weights from sensors to first hidden layer, 
        # from last hidden layer to motors, 
        # and from each hidden layer to the next
            for layer in range(numLayers):
                if layer == 0:
                    self.weights[layer] = np.random.rand(numSensorNeurons,c.hiddenNeurons[layer]) * 2 - 1
                elif layer == numLayers - 1:
                    self.weights[layer] = np.random.rand(c.hiddenNeurons[layer-1],numMotorNeurons) * 2 - 1
                else:
                    self.weights[layer] = np.random.rand(c.hiddenNeurons[layer-1],c.hiddenNeurons[layer]) * 2 - 1

    def Create_World(self):
        """
        Creates a world for the simulation. Currently, this is just a blank world.

        @return: None
        """
        pyrosim.Start_SDF("src/robotfiles/world.sdf")
        pyrosim.End()

    def Create_Body(self,save:bool):
        """
        Creates a body for the individual.

        Parameters:
        @save: if True, saves the body in the folder specified by c.savedPath. This is usually used for the best individual of the search process.

        Returns: None
        """

        def Get_Link_Color(linkName:str):
            """
            Gets the color of the link, dependent on whether or not it has a sensor. If it has a sensor, it is green. Otherwise, it is cyan.

            @linkName: the name of the link

            @return: the color of the link
            """
            if linkName in self.sensorLinks:
                return "Green"
            else:
                return "Cyan"

        if save:
            filePath = f"{c.savedPath}body/{self.myID}.urdf"
        else:
            filePath = f"{c.tempfilePath}body/{self.myID}.urdf"

        pyrosim.Start_URDF(filePath)

        # get the greatest link z size
        maxHeight = max(self.linksToLengths.values(), key = lambda x: x[2])[2]
        firstYLength = self.linksToLengths[self.linkNames[0]][1]

        # send the first link and first joint, with absolute position
        #! joint type and axis are hardcoded for now, don't matter for assignment 6
        pyrosim.Send_Cube(name=self.linkNames[0],pos=[0,0,maxHeight/2],size=self.linksToLengths[self.linkNames[0]],color=Get_Link_Color(self.linkNames[0]))
        pyrosim.Send_Joint(name=self.jointNames[0],parent=self.linkNames[0],child=self.linkNames[1],type="fixed",jointAxis="1 0 0",position=[0,firstYLength/2,maxHeight/2])

        # send the middle links and joints, with relative position
        for i in range(1,self.numLinks-1):
            yLength = self.linksToLengths[self.linkNames[i]][1]
            pyrosim.Send_Cube(name=self.linkNames[i],pos=[0,yLength/2,0],size=self.linksToLengths[self.linkNames[i]],color=Get_Link_Color(self.linkNames[i]))
            pyrosim.Send_Joint(name=self.jointNames[i],parent=self.linkNames[i],child=self.linkNames[i+1],type="fixed",jointAxis="1 0 0",position=[0,yLength,0])

        # send the last link with relative position
        lastYLength = self.linksToLengths[self.linkNames[-1]][1]
        pyrosim.Send_Cube(name=self.linkNames[-1],pos=[0,lastYLength/2,0],size=self.linksToLengths[self.linkNames[-1]],color=Get_Link_Color(self.linkNames[-1]))
        pyrosim.End()


    def Create_Brain(self,save:bool):
        """ 
        Creates a neural network for the individual, saving it in a temporary .nndf file.

        Parameters:
        @save: if True, saves the brain in the folder specified by c.savedPath. This is usually used for the best individual of the search process.
        Returns: None
        """

        def Get_Cumulative_Hidden_Neuron_Count(layer):
            if layer < 0:
                return 0
            if layer == 0:
                return c.hiddenNeurons[layer]
            return c.hiddenNeurons[layer] + Get_Cumulative_Hidden_Neuron_Count(layer-1)

        # if save == True, send the brain to the folder specified by c.savedPath
        if save:
            filePath = f"{c.savedPath}brain/{self.myID}.nndf"
        else:
            filePath = f"{c.tempfilePath}brain/{self.myID}.nndf"

        pyrosim.Start_NeuralNetwork(filePath)
        numMotorNeurons = self.numLinks - 1
        numSensorNeurons = len(self.sensorLinks)
        sensorLinks = list(self.sensorLinks)

        # send a sensor neuron to each link
        for linkName in self.sensorLinks:
            pyrosim.Send_Sensor_Neuron(name=linkName,linkName=str(linkName))
        
        # send all hidden neurons, layer agnostic for now
        totalHiddenNeurons = sum(c.hiddenNeurons.values())
        i = self.numLinks
        for _ in range(totalHiddenNeurons):
            pyrosim.Send_Hidden_Neuron(name=i)
            i += 1

        # send a motor neuron to each joint
        for jointName in self.jointNames:
            pyrosim.Send_Motor_Neuron(name=i,jointName=jointName)
            i += 1

        # if there are no hidden layers, just send synapses from sensors to motors
        if len(c.hiddenNeurons) == 0:
            for i in range(numSensorNeurons):
                for j in range(numMotorNeurons):
                    pyrosim.Send_Synapse(sourceNeuronName=sensorLinks[i], targetNeuronName=self.numLinks+j,weight=self.weights[0][i,j])
        # if there is only one hidden layer, send synapses from sensors to first hidden layer, then from first hidden layer to motors
        elif len(c.hiddenNeurons) == 1:
            for i in range(numSensorNeurons):
                for j in range(c.hiddenNeurons[0]):
                    pyrosim.Send_Synapse(sourceNeuronName=sensorLinks[i], targetNeuronName=self.numLinks+j,weight=self.weights[0][i,j])

            for i in range(c.hiddenNeurons[0]):
                for j in range(numMotorNeurons):
                    pyrosim.Send_Synapse(sourceNeuronName=i+self.numLinks, targetNeuronName=self.numLinks+c.hiddenNeurons[0]+j,weight=self.weights[1][i,j])
        # if there is more than one hidden layer, link synapses from sensors -> hidden layers -> motors
        else:
            for layer in range(len(c.hiddenNeurons)):
                # send synapses from sensors to first hidden layer
                if layer == 0:
                    for i in range(numSensorNeurons):
                        for j in range(c.hiddenNeurons[0]):
                            pyrosim.Send_Synapse(sourceNeuronName=sensorLinks[i], targetNeuronName=self.numLinks+j,weight=self.weights[0][i,j])
                else:
                    for i in range(c.hiddenNeurons[layer-1]):
                        for j in range(c.hiddenNeurons[layer]):
                            pyrosim.Send_Synapse(sourceNeuronName=i+self.numLinks+Get_Cumulative_Hidden_Neuron_Count(layer-2), targetNeuronName=self.numLinks+Get_Cumulative_Hidden_Neuron_Count(layer-1)+j,weight=self.weights[layer][i,j])
            # send synapses from last hidden layer to motors     
            for i in range(c.hiddenNeurons[len(c.hiddenNeurons)-1]):
                for j in range(numMotorNeurons):
                    pyrosim.Send_Synapse(sourceNeuronName=i+self.numLinks+Get_Cumulative_Hidden_Neuron_Count(len(c.hiddenNeurons)-2), targetNeuronName=self.numLinks+Get_Cumulative_Hidden_Neuron_Count(len(c.hiddenNeurons)-1)+j,weight=self.weights[len(c.hiddenNeurons)-1][i,j])

        pyrosim.End()
        return


    def Start_Simulation(self,directOrGUI,save=False):
        if directOrGUI != "DIRECT" and directOrGUI != "GUI":
            print("parameter must be DIRECT or GUI")
            exit()
        
        if save:
            # when save is True, we don't need to run async, so we can just run the simulation here
            self.Create_Brain(save=True)
            self.Create_Body(save=True)
            simulation = SIMULATION(directOrGUI,self.myID,savedName=str(self.myID))
            simulation.Run()
            simulation.Get_Fitness()
        else:
            self.Create_Body(save=False)
            self.Create_Brain(save=False)
            os.system(f"python3 src/simulate.py {directOrGUI} {self.myID} 2&>output.txt &")
 
    def Wait_For_Simulation_To_End(self,save=False):
        fitnessFileName = f"{c.tempfilePath}fitness/{self.myID}.txt"
        while not os.path.exists(fitnessFileName):
            time.sleep(0.2)
        while True:
            f = open(fitnessFileName,"r")
            content = f.read()
            if content != "":
                self.fitness = float(content)
                f.close()
                break
            else:
                f.close()
        time.sleep(0.03)
        if save:
            os.system(f"mv {fitnessFileName} {c.savedPath}fitness/{self.myID}.txt")
        else:
            os.system(f"rm {fitnessFileName}")

    def Mutate(self):
        for layer, weights in self.weights.items():
            for i in range(weights.shape[0]):
                for j in range(weights.shape[1]):
                    if random.random() < c.mutationRate:
                        self.weights[layer][i,j] += self.weights[layer][i,j] * random.gauss(0,1) * c.mutationPower

    def Set_ID(self,new_id):
        self.myID = new_id