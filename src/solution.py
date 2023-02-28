import numpy as np
import src.pyrosim.pyrosim as pyrosim
import os
import copy
from pprint import pprint
import random
import src.constants as c
from src.simulation import SIMULATION
from src.joint import JOINT
from src.link import LINK
import time

#TODO: add docstrings for all functions
class SOLUTION:
    def __init__(self,sol_id:id, isOriginal:bool=False):
        #TODO: add doctsring
        #TODO: add comments
        if isOriginal:
            self.myID = sol_id
            self.numLinks = np.random.randint(c.minLinks,c.maxLinks)
            self.joints = {}
            self.links = {}
            
            # create the root link
            rootLink = LINK(None,0)
            self.links[rootLink.name] = rootLink

            while len(self.links) < self.numLinks:
                links = list(self.links.keys())
                weights = [6-len(self.links[link].connectedFaces) for link in links]
                weights /= np.sum(weights)
                randomParent = np.random.choice(links,p=weights)

                availableKeys = set(c.faces.keys()) - (set(c.faces.keys()) & self.links[randomParent].connectedFaces)
                if len(availableKeys) < 4:
                    # print("no available keys for parent",randomParent,"connected faces",self.links[randomParent].connectedFaces)
                    continue
                
                randomFace = np.random.choice(list(availableKeys))
                
                newJoint = JOINT(self.links[randomParent],randomFace)
                
                newChild = LINK(newJoint,len(self.links))
                
                newJoint.addChild(newChild)
                
                overlapsAnyLinks = any([newChild.spacesOverlap(link) for link in self.links.values()])

                if not overlapsAnyLinks:
                    self.links[newChild.name] = newChild
                    self.joints[newJoint.name] = newJoint
                    self.links[randomParent].addConnectedFace(randomFace)

            self.sensorLinks = set()
            self.Get_Sensor_Links()

            self.weights = dict()
            # create random weights dependent on number of neurons
            self.Create_Weights()
        else:
            pass

    def __lt__(self,other):
        return self.fitness < other.fitness
    
    def inheritFromParent(self,parent):
        #TODO: add doctsring
        #TODO: add comments
        #TODO: add type annotations
        self.myID = parent.myID
        self.numLinks = parent.numLinks
        self.joints = copy.deepcopy(parent.joints)
        self.links = copy.deepcopy(parent.links)
        self.sensorLinks = copy.deepcopy(parent.sensorLinks)
        self.weights = copy.deepcopy(parent.weights)
        # print("child num links: ",self.numLinks)

    def Get_Sensor_Links(self):
        """
        Randomly choose which links will have sensors. Updates `self.sensorLinks` to contain the names of the links that will have sensors.

        @return: `None`
        """
        # get the proportion of links that will have sensors
        sensorProportion = np.random.uniform(c.minSensorProportion,c.maxSensorProportion)
        # get the number of links that will have sensors -> will be at least 1
        numSensorLinks = max(int(sensorProportion * self.numLinks),1)
        # choose which links will have sensors
        indices = np.random.choice(self.numLinks,numSensorLinks,replace=False)
        # add the names of the links that will have sensors to the set of sensor links
        self.sensorLinks |= set(indices)

    def Create_Weights(self):
        """
        Initializes random weights for the neural network, saving them in the `self.weights` dictionary.

        The dictionary is structured as follows: keys are the layer number, and values are each a matrix of weights, 
        `matrix[i][j]` being the weight from the `ith` neuron in the layer to the `jth` neuron in the next layer.

        @return: `None`
        """
        numLayers = len(c.hiddenNeurons)
        numSensorNeurons = len(self.sensorLinks)
        numMotorNeurons = len(self.joints)
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

    def Create_Body(self,save:bool):
        """
        Creates a body for the individual.

        
        @param `save`: if `True`, saves the body in the folder specified by `c.savedPath`. This is usually used for the best individual of the search process.

        @return: `None`
        """

        def Get_Link_Color(linkName:str):
            """
            Gets the color of the link, dependent on whether or not it has a sensor. If it has a sensor, it is green. Otherwise, it is cyan.

            @param `linkName`: the name of the link

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

        for link in self.links.values():
            pyrosim.Send_Cube(name=str(link.name),pos=link.relativePosition,size=link.dims,color=Get_Link_Color(link.name))
        
        for joint in self.joints.values():
            pyrosim.Send_Joint(name=str(joint.name),parent=str(joint.parent.name),child=str(joint.child.name),position=joint.position,jointAxis=joint.axis,type=joint.type)

        pyrosim.End()

    def Create_Brain(self,save:bool):
        """ 
        Creates a neural network for the individual, saving it in a temporary .nndf file.

        
        @param `save`: if True, saves the brain in the folder specified by c.savedPath. This is usually used for the best individual of the search process.

        @return: `None`
        """

        def Get_Cumulative_Hidden_Neuron_Count(layer:int):
            """
            Gets the cumulative number of hidden neurons up to the specified layer.

            @param `layer`: the layer number

            @return: the cumulative number of hidden neurons up to the specified layer
            """
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
        numMotorNeurons = len(self.joints)
        numSensorNeurons = len(self.sensorLinks)
        sensorLinks = sorted(self.sensorLinks)

        # send a sensor neuron to each link
        for linkName in self.sensorLinks:
            pyrosim.Send_Sensor_Neuron(name=linkName,linkName=str(linkName))
        
        # send all hidden neurons, layer agnostic for now
        totalHiddenNeurons = sum(c.hiddenNeurons.values())
        numLinks = len(self.links)
        i = numLinks
        for _ in range(totalHiddenNeurons):
            pyrosim.Send_Hidden_Neuron(name=i)
            i += 1

        # send a motor neuron to each joint
        for jointName in sorted(self.joints.keys()):
            pyrosim.Send_Motor_Neuron(name=i,jointName=jointName)
            i += 1

        # if there are no hidden layers, just send synapses from sensors to motors
        if len(c.hiddenNeurons) == 0:
            for i in range(numSensorNeurons):
                for j in range(numMotorNeurons):
                    #!
                    try:
                        pyrosim.Send_Synapse(sourceNeuronName=sensorLinks[i], targetNeuronName=numLinks+j,weight=self.weights[0][i,j])
                    except Exception as e:
                        print("exception occured: ",e)
                        print(self.links)
                        print(sensorLinks)
                        print(i)
                        exit()
        # if there is only one hidden layer, send synapses from sensors to first hidden layer, then from first hidden layer to motors
        elif len(c.hiddenNeurons) == 1:
            for i in range(numSensorNeurons):
                for j in range(c.hiddenNeurons[0]):
                    #!
                    try:
                        pyrosim.Send_Synapse(sourceNeuronName=sensorLinks[i], targetNeuronName=numLinks+j,weight=self.weights[0][i,j])
                    except Exception as e:
                        print("exception occured: ",e)
                        pprint(self.links)
                        pprint(sensorLinks)
                        print(i)
                        pprint(self.weights)
                        exit()
                    
            for i in range(c.hiddenNeurons[0]):
                for j in range(numMotorNeurons):
                    pyrosim.Send_Synapse(sourceNeuronName=i+numLinks, targetNeuronName=numLinks+c.hiddenNeurons[0]+j,weight=self.weights[1][i,j])
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
        #TODO: add docstring
        #TODO: add comments
        if directOrGUI != "DIRECT" and directOrGUI != "GUI":
            print("parameter must be DIRECT or GUI")
            exit()

        #! this is really just for debugging so that things are printed to the terminal
        hideOutput = "2&>output.txt"
        hideOutput = ""
        
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
            os.system(f"python3 -m src.simulate {directOrGUI} {self.myID} {hideOutput} &")
 
    def Wait_For_Simulation_To_End(self,save=False):
        #TODO: add docstring
        #TODO: add comments
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

    def mutateWeights(self):
        """
        Randomly mutates weights in `self.weights` based on chance and magnitude specified in `src/constants.py`.

        @return: `None`
        """
        for layer, weights in self.weights.items():
            for i in range(weights.shape[0]):
                for j in range(weights.shape[1]):
                    if random.random() < c.mutationRate:
                        self.weights[layer][i,j] += self.weights[layer][i,j] * random.gauss(0,1) * c.mutationPower

    def flipSensors(self):
        """
        Randomly flips whether or not a link is a sensor link, based on chance specified in `src/constants.py`. Updates `self.weights` accordingly.

        @return: `None`
        """
        for link in self.links:
            # for each link, with probability c.flipSensorLinkChance, flip whether or not it is a sensor link
            if np.random.rand() < c.flipSensorLinkChance:
                # if the link is already a sensor link, remove it from the set of sensor links and remove the corresponding weights (only if there is more than one sensor link)
                if link in self.sensorLinks and len(self.sensorLinks) > 1:
                    self.removeSensorWeights(sorted(self.sensorLinks).index(link))
                    #!
                    # print("removing sensor link:", link)
                    # print(self.sensorLinks)
                    # pprint(self.weights[0])
                    # print()
                    self.sensorLinks.remove(link)
                elif link not in self.sensorLinks:
                    # if the link is not a sensor link, add it to the set of sensor links and add the corresponding weights
                    #!
                    # print("adding sensor link:", link)
                    # print(self.sensorLinks)
                    self.sensorLinks.add(link)
                    # print(self.sensorLinks)
                    # print()
                    self.addSensorWeights(sorted(self.sensorLinks).index(link))

                self.exceptNonMatchingSensorWeights("flipSensors")

    def mutateBody(self):
        """
        With probabilities provided in `src/constants.py`, adds a link, or removes an external link, updating `self.weights` accordingly.

        @return: `None`
        """
        # with probability c.removeLinkChance, remove a link if doing so would not cause the body to have less than c.minLinks
        if np.random.rand() < c.removeLinkChance and len(self.links) > c.minLinks:
            # get the external links (only connected to one other link). If there are none, then we can't remove a link. Never remove the root link
            outsideLinks = {linkName for linkName, link in self.links.items() if len(link.connectedFaces) == 1 and link.upstreamJoint is not None}
            if len(outsideLinks) > 0:
                # choose a random link to remove
                linkToRemove = np.random.choice(list(outsideLinks))
                upstreamJointToRemove = self.links[linkToRemove].upstreamJoint
                parent = upstreamJointToRemove.parent
                
                # update the connected faces of the parent to reflect removal of the link connected to its face
                if parent is not None:
                    parent.removeConnectedFace(upstreamJointToRemove.face)
                # remove the link from the links dictionary
                del self.links[linkToRemove]
                if linkToRemove in self.sensorLinks:
                    # remove the weights associated with the sensor link
                    self.removeSensorWeights(sourceIdx=sorted(self.sensorLinks).index(linkToRemove))
                    # remove the sensor link from the sensor link set
                    self.sensorLinks.remove(linkToRemove)
                    self.exceptNonMatchingSensorWeights("mutateBody (remove)")

                # remove the joint from the joints dictionary
                motorToRemove = sorted(self.joints).index(upstreamJointToRemove.name)
                self.removeMotorWeights(motorToRemove)
                del self.joints[upstreamJointToRemove.name]

                self.exceptNonMatchingMotorWeights("mutateBody (remove)")

        if np.random.rand() < c.addLinkChance and len(self.links) < c.maxLinks:
            #TODO: add a new link, becoming a sensor weight with random chance. If it is, update the weights matrix accordingly. Update the joints and links dictionaries accordingly, and update the motor weights as well
            pass

    def addMotorWeights(self,motorIdx:int):
        """
        Adds a new column of random weights in the last weight layer into `self.weights`, corresponding to the new joint.

        @param `motorIdx`: the index of the new motor

        @return: `None`
        """
        lastLayer = len(self.weights) - 1
        newCol = np.random.rand(self.weights[lastLayer].shape[0],1) * 2 -1
        newWeights = np.insert(self.weights[lastLayer],motorIdx,newCol,axis=1)
        self.weights[lastLayer] = newWeights

    def removeMotorWeights(self,motorIdx:int):
        """
        Removes a column of weights in the last weight layer from `self.weights`, corresponding to the removed joint.

        @param `motorIdx`: the index of the motor to remove

        @return: `None` 
        """
        lastLayer = len(self.weights) - 1
        newWeights = np.delete(self.weights[lastLayer],motorIdx,axis=1)
        self.weights[lastLayer] = newWeights

    def addSensorWeights(self,sourceIdx:int):
        """
        Adds a new row of weights for the inserted sensor link to the weights matrix. The new row of weights is a random vector of length equal to the number of neurons in the next layer, which is the first hidden layer if there are hidden layers or the motor layer if there are no hidden layers.

        @param `sourceIdx`: the index of the new sensor link in the sensorLinks list

        @return: `None`
        """
        # create newWeights, a row vector of length equal to the number of neurons in the next layer, which is the first hidden layer if there are hidden layers or the motor layer if there are no hidden layers
        if len(c.hiddenNeurons) > 0:
            newWeights = np.random.rand(c.hiddenNeurons[0]) * 2 - 1
        else:
            newWeights = np.random.rand(len(self.joints)) * 2 - 1
        # insert the new weights into the weights matrix
        self.weights[0] = np.insert(self.weights[0],sourceIdx,newWeights,axis=0)

    def removeSensorWeights(self,sourceIdx:int):
        """
        Removes the row of weights associated with the sensor link at the given index in the sensorLinks list.

        @param `sourceIdx`: the index of the sensor link in the sensorLinks list

        @return: `None`
        """
        # remove the row of weights associated with the sourceIdx
        newWeights = np.delete(self.weights[0],sourceIdx,axis=0)
        try:
            assert newWeights.shape[0] == self.weights[0].shape[0] - 1, f"newWeights.shape[0] = {newWeights.shape[0]}, self.weights[0].shape[0] = {self.weights[0].shape[0]}. These should be equal."
        except AssertionError as e:
            print(f"removeSensorWeights: {e}")
            exit()
        self.weights[0] = newWeights
        

    def Set_ID(self,new_id:int):
        """
        Sets `self.myID` to the given ID.

        @param `new_id`: the new ID

        @return: `None`
        """
        self.myID = new_id

    def exceptNonMatchingSensorWeights(self,funcName:str):
        """
        Try-except wrapper to check that sensor weight matrix has the correct number of rows.

        @param `funcName`: the name of the function that called this function

        @return: `None`
        """
        try:
            assert len(self.sensorLinks) == self.weights[0].shape[0], f"len(self.sensorLinks) = {len(self.sensorLinks)}, self.weights[0].shape[0] = {self.weights[0].shape[0]}. These should be equal."
        except AssertionError as e:
            print(f"{funcName}: {e}")
            print(self.sensorLinks)
            pprint(self.weights[0])
            exit()

    def exceptNonMatchingMotorWeights(self,funcName:str):
        """
        Try-except wrapper to check that motor weight matrix has the correct number of columns.

        @param `funcName`: the name of the function that called this function

        @return: `None`
        """
        try:
            assert len(self.joints) == self.weights[len(self.weights)-1].shape[1], f"len(self.joints) = {len(self.joints)}, self.weights[len(self.weights)-1].shape[1] = {self.weights[len(self.weights)-1].shape[1]}. These should be equal."
        except AssertionError as e:
            print(f"{funcName}: {e}")
            print(self.joints)
            pprint(self.weights[len(self.weights)-1])
            exit()
        