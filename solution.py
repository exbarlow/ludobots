import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import constants as c
import time

class SOLUTION:
    def __init__(self,sol_id):
        self.weights = dict()
        self.linkNames = []
        self.jointNames = []
        self.myID = sol_id
        self.Create_Weights()
        

    def __lt__(self,other):
        return self.fitness < other.fitness

    def Create_Weights(self):
        numLayers = len(c.hiddenNeurons)
        # If there is no hidden layer, just create weights from sensors to motors
        if numLayers == 0:
            self.weights[0] = np.random.rand(c.numSensorNeurons,c.numMotorNeurons)
            return 
        # Else, we will create weights from sensors to first hidden layer, 
        # from last hidden layer to motors, 
        # and from each hidden layer to the next
        for layer in range(numLayers):
            if layer == 0:
                self.weights[layer] = np.random.rand(c.numSensorNeurons,c.hiddenNeurons[layer])
            elif layer == numLayers - 1:
                self.weights[layer] = np.random.rand(c.hiddenNeurons[layer-1],c.numMotorNeurons)
            else:
                self.weights[layer] = np.random.rand(c.hiddenNeurons[layer-1],c.hiddenNeurons[layer])

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")

        pyrosim.Send_Cube(name="Center",pos=[0,0,10],size=[0.5,0.5,0.5])
        self.linkNames.append("Center")

        pyrosim.Send_Joint(name="Center_MiddleFront",parent="Center",child="MiddleFront",position=[0,0.25,10],type="revolute",jointAxis="1 0 0")
        pyrosim.Send_Cube(name="MiddleFront",pos=[0,0.25,0],size=[0.5,0.5,0.5])
        self.jointNames.append("Center_MiddleFront")
        self.linkNames.append("MiddleFront")

        pyrosim.Send_Joint(name="MiddleFront_Front",parent="MiddleFront",child="Front",position=[0,0.25,0],type="revolute",jointAxis="1 0 0")
        pyrosim.Send_Cube(name="Front",pos=[0,0.25,0],size=[0.5,0.5,0.5])
        self.jointNames.append("MiddleFront_Front")
        self.linkNames.append("Front")

        pyrosim.Send_Joint(name="Center_MiddleBack",parent="Center",child="MiddleBack",position=[0,-0.25,10],type="revolute",jointAxis="1 0 0")
        pyrosim.Send_Cube(name="MiddleBack",pos=[0,-0.25,0],size=[0.5,0.5,0.5])
        self.jointNames.append("Center_MiddleBack")
        self.linkNames.append("MiddleBack")

        pyrosim.Send_Joint(name="MiddleBack_Back",parent="MiddleBack",child="Back",position=[0,-0.25,0],type="revolute",jointAxis="1 0 0")
        pyrosim.Send_Cube(name="Back",pos=[0,-0.25,0],size=[0.5,0.5,0.5])
        self.jointNames.append("MiddleBack_Back")
        self.linkNames.append("Back")

        pyrosim.Send_Joint(name="Center_RightWingConnector",parent="Center",child="RightWingConnector",position=[0.25,0,10],type="revolute",jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightWingConnector",pos=[0.5,0,0],size=[1,1,0.25])
        self.jointNames.append("Center_RightWingConnector")
        self.linkNames.append("RightWingConnector")

        pyrosim.Send_Joint(name="Center_LeftWingConnector",parent="Center",child="LeftWingConnector",position=[-0.25,0,10],type="revolute",jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LeftWingConnector",pos=[-0.5,0,0],size=[1,1,0.25])
        self.jointNames.append("Center_LeftWingConnector")
        self.linkNames.append("LeftWingConnector")

        pyrosim.End()



    def Create_Brain(self,save:bool):
        """ Creates a neural network for the individual, saving it in a temporary .nndf file.

        Parameters:
            save: if True, saves the brain in the folder specified by c.savedPath. 
                    This is usually used for the best individual of the search process.
        Returns:
            None
        """

        def Get_Cumulative_Hidden_Neuron_Count(layer):
            if layer == 0:
                return c.hiddenNeurons[layer]
            return c.hiddenNeurons[layer] + Get_Cumulative_Hidden_Neuron_Count(layer-1)

        # if save == True, send the brain to the folder specified by c.savedPath
        folder = ""
        if save:
            folder = c.savedPath
        pyrosim.Start_NeuralNetwork(f"{folder}brain{self.myID}.nndf")

        # send a sensor neuron to each link
        i = 0
        for linkName in self.linkNames:
            pyrosim.Send_Sensor_Neuron(name=i,linkName=linkName)
            i += 1
        
        # send all hidden neurons, layer agnostic for now
        totalHiddenNeurons = sum(c.hiddenNeurons.values())
        for _ in range(totalHiddenNeurons):
            pyrosim.Send_Hidden_Neuron(name=i)
            i += 1

        # send a motor neuron to each joint
        for jointName in self.jointNames:
            pyrosim.Send_Motor_Neuron(name=i,jointName=jointName)
            i += 1

        # if there are no hidden layers, just send synapses from sensors to motors
        if len(c.hiddenNeurons) == 0:
            for i in range(c.numSensorNeurons):
                for j in range(c.numMotorNeurons):
                    pyrosim.Send_Synapse(sourceNeuronName=i, targetNeuronName=c.numSensorNeurons+j,weight=self.weights[0][i,j])
            pyrosim.End()
            return
        # else, we involve the hidden neurons
        else:
            for layer in range(len(c.hiddenNeurons)-1):
                # send synapses from sensors to first hidden layer
                if layer == 0:
                    for i in range(c.numSensorNeurons):
                        for j in range(c.hiddenNeurons[0]):
                            pyrosim.Send_Synapse(sourceNeuronName=i, targetNeuronName=c.numSensorNeurons+j,weight=self.weights[0][i,j])
                else:
                    for i in range(c.hiddenNeurons[layer-1]):
                        for j in range(c.hiddenNeurons[layer]):
                            pyrosim.Send_Synapse(sourceNeuronName=i, targetNeuronName=c.numSensorNeurons+Get_Cumulative_Hidden_Neuron_Count(layer-1)+j,weight=self.weights[layer][i,j])
            # send synapses from last hidden layer to motors     
            for i in range(c.hiddenNeurons[len(c.hiddenNeurons)-1]):
                for j in range(c.numMotorNeurons):
                    pyrosim.Send_Synapse(sourceNeuronName=i, targetNeuronName=c.numSensorNeurons+totalHiddenNeurons+j,weight=self.weights[len(c.hiddenNeurons)-1][i,j])

        pyrosim.End()
        exit()
        return


    def Start_Simulation(self,directOrGUI,save=False):
        if directOrGUI != "DIRECT" and directOrGUI != "GUI":
            print("parameter must be DIRECT or GUI")
            exit()
            
        self.Create_Brain(save=False)
        runAsync = "&"
        if save:
            runAsync = ""
            self.Create_Brain(save=True)
        
        os.system(f"python3 simulate.py {directOrGUI} {self.myID} 2&>output {runAsync}")
 
    def Wait_For_Simulation_To_End(self):
        fitnessFileName = f"fitness{self.myID}.txt"
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
        os.system(f"rm {fitnessFileName}")

    def Mutate(self):
        rows, cols = self.weights.shape
        randomRow = random.randint(0,rows-1)
        randomColumn = random.randint(0,cols-1)
        self.weights[randomRow,randomColumn] = random.random() * 2 - 1

    def Set_ID(self,new_id):
        self.myID = new_id