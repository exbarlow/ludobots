from solution import SOLUTION
import constants as c
import copy
import os

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        # self.parent = SOLUTION()
        os.system("rm fitness*.txt")
        os.system("rm brain*.nndf")
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
        

    def Evolve(self):
        for parent in self.parents.values():
            parent.Start_Simulation("DIRECT")

        for parent in self.parents.values():
            parent.Wait_For_Simulation_To_End()

        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation(currentGeneration)

    def Evolve_For_One_Generation(self,currentGeneration):
        self.Spawn()
        self.Mutate()
        # if currentGeneration == 0: 
        #     self.child.Evaluate("GUI")
        # else:
        #     self.child.Evaluate("DIRECT")

        # self.Print()
        # self.Select()

    def Spawn(self):
        self.children = {}
        print(len(self.parents))
        for i in range(len(self.parents)):
            self.children[i] = copy.deepcopy(list(self.parents.values())[i])
            self.children[i].Set_ID(self.nextAvailableID)
            self.nextAvailableID+=1
        # for key, val in self.children.items():
        #     print(key,val)
        # exit()

    def Mutate(self):
        for child in self.children:
            child.Mutate()

    def Select(self):
        if self.parent.fitness > self.child.fitness:
            self.parent = self.child

    def Print(self):
        print(self.parent.fitness,self.child.fitness)

    def Show_Best(self):
        # self.parent.Evaluate("GUI")
        pass


