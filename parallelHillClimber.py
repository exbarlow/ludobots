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
        
    def Evaluate(self,solutions):
        for parent in solutions.values():
            parent.Start_Simulation("DIRECT")

        for parent in solutions.values():
            parent.Wait_For_Simulation_To_End()

    def Evolve(self):
        self.Evaluate(self.parents)

        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation(currentGeneration)

    def Evolve_For_One_Generation(self,currentGeneration):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        # self.Print()
        self.Select()

    def Spawn(self):
        self.children = {}
        for parentID, parent in self.parents.items():
            self.children[parentID] = copy.deepcopy(parent)
            self.children[parentID].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for child in self.children.values():
            child.Mutate()

    def Select(self):
        for parentID in self.parents:
            if self.parents[parentID].fitness > self.children[parentID].fitness:
                self.parents[parentID] = self.children[parentID]

    def Print(self):
        for parentID in self.parents:
            print("\nparent fitness:", self.parents[parentID].fitness)
            print("child fitness:",self.children[parentID].fitness,"\n")
        # print(self.parent.fitness,self.child.fitness)

    def Show_Best(self):
        min(self.parents.values()).Start_Simulation("GUI",isBest=True)
        exit()



