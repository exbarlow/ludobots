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

        pyrosim.Send_Cube(name="Box",pos=[3,3,0.5],size=[1,1,1])

        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")

        pyrosim.Send_Cube(name="Torso",pos=[0,0,1],size=[1,1,1])
        pyrosim.Send_Joint(name="Torso_BackLeg",
                           parent="Torso",
                           child="BackLeg",
                           type="revolute",
                           position=[0,-0.5,1],
                           jointAxis="1 0 0")
        pyrosim.Send_Cube(name="BackLeg",pos=[0,-0.5,0],size=[0.2,1,0.2])
        pyrosim.Send_Joint(name="Torso_FrontLeg",
                           parent="Torso",
                           child="FrontLeg",
                           type="revolute",
                           position=[0,0.5,1],
                           jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLeg",pos=[0,0.5,0],size=[0.2,1,0.2])

        pyrosim.End()


    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")

        pyrosim.Send_Sensor_Neuron(name=0,linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1,linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=2,linkName="FrontLeg")

        pyrosim.Send_Motor_Neuron(name=3,jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=4,jointName="Torso_FrontLeg")

        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow,
                                    targetNeuronName=currentColumn+c.numSensorNeurons,
                                    weight=self.weights[currentRow][currentColumn])

        pyrosim.End()


    def Start_Simulation(self,directOrGUI):
        if directOrGUI != "DIRECT" and directOrGUI != "GUI":
            print("parameter must be DIRECT or GUI")
            exit()
            
        # self.Create_World()
        # self.Create_Body()
        self.Create_Brain()
        os.system(f"python3 simulate.py {directOrGUI} {self.myID} 2&>erroutput & ")

    def Wait_For_Simulation_To_End(self):
        fitnessFileName = f"fitness{self.myID}.txt"
        while not os.path.exists(fitnessFileName):
            time.sleep(1)
        f = open(fitnessFileName,"r")
        self.fitness = float(f.read())
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