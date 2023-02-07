import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import constants as c
import time

class SOLUTION:
    def __init__(self,sol_id):
        self.weights = np.random.rand(c.numSensorNeurons,c.numMotorNeurons)
        self.weights = self.weights * 2 - 1
        self.myID = sol_id

    def __lt__(self,other):
        return self.fitness < other.fitness

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")

        # pyrosim.Send_Cube(name="Platform",pos=[0,0,2.5],size=[10,10,5],mass=0)

        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")

        pyrosim.Send_Cube(name="Center",pos=[0,0,10],size=[0.5,0.5,0.5])

        pyrosim.Send_Joint(name="Center_MiddleFront",parent="Center",child="MiddleFront",position=[0,0.25,10],type="revolute",jointAxis="1 0 0")
        pyrosim.Send_Cube(name="MiddleFront",pos=[0,0.25,0],size=[0.5,0.5,0.5])

        pyrosim.Send_Joint(name="MiddleFront_Front",parent="MiddleFront",child="Front",position=[0,0.25,0],type="revolute",jointAxis="1 0 0")
        pyrosim.Send_Cube(name="Front",pos=[0,0.25,0],size=[0.5,0.5,0.5])

        pyrosim.Send_Joint(name="Center_MiddleBack",parent="Center",child="MiddleBack",position=[0,-0.25,10],type="revolute",jointAxis="1 0 0")
        pyrosim.Send_Cube(name="MiddleBack",pos=[0,-0.25,0],size=[0.5,0.5,0.5])

        pyrosim.Send_Joint(name="MiddleBack_Back",parent="MiddleBack",child="Back",position=[0,-0.25,0],type="revolute",jointAxis="1 0 0")
        pyrosim.Send_Cube(name="Back",pos=[0,-0.25,0],size=[0.5,0.5,0.5])

        pyrosim.Send_Joint(name="Center_RightWingConnector",parent="Center",child="RightWingConnector",position=[0.25,0,10],type="revolute",jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightWingConnector",pos=[0.5,0,0],size=[1,1,0.25])

        # pyrosim.Send_Joint(name="RightWingConnector_RightWing",parent="RightWingConnector",child="RightWing",position=[0.125,0,0],type="fixed",jointAxis="1 0 0")
        # pyrosim.Send_Cube(name="RightWing",pos=[1,0,0],size=[2,1.5,0.1])

        pyrosim.Send_Joint(name="Center_LeftWingConnector",parent="Center",child="LeftWingConnector",position=[-0.25,0,10],type="revolute",jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LeftWingConnector",pos=[-0.5,0,0],size=[1,1,0.25])

        # pyrosim.Send_Joint(name="LeftWingConnector_LeftWing",parent="LeftWingConnector",child="LeftWing",position=[-0.125,0,0],type="fixed",jointAxis="1 0 0")
        # pyrosim.Send_Cube(name="LeftWing",pos=[-1,0,0],size=[2,1.5,0.1])

        pyrosim.End()


    def Create_Brain(self,save):

        folder = ""
        if save:
            folder = c.savedPath
        pyrosim.Start_NeuralNetwork(f"{folder}brain{self.myID}.nndf")

        i = 0
        for linkName in ["Center","MiddleFront","Front","MiddleBack","Back","RightWingConnector","LeftWingConnector"]:
            pyrosim.Send_Sensor_Neuron(name=i,linkName=linkName)
            i += 1
        for jointName in ["Center_MiddleFront","MiddleFront_Front","Center_MiddleBack","MiddleBack_Back","Center_RightWingConnector","Center_LeftWingConnector"]:
            pyrosim.Send_Motor_Neuron(name=i,jointName=jointName)
            i += 1


        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow,
                                    targetNeuronName=currentColumn+c.numSensorNeurons,
                                    weight=self.weights[currentRow][currentColumn])

        pyrosim.End()


    def Start_Simulation(self,directOrGUI,save=False):
        if directOrGUI != "DIRECT" and directOrGUI != "GUI":
            print("parameter must be DIRECT or GUI")
            exit()
            
        # self.Create_World()
        # self.Create_Body()
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