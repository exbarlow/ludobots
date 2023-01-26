from solution import SOLUTION
import constants as c
import copy

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        # self.parent = SOLUTION()
        self.parents = dict()
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION()

    def Evolve(self):
        for parent in self.parents.values():
            parent.Evaluate("GUI")
        # for currentGeneration in range(c.numberOfGenerations):
        #     self.Evolve_For_One_Generation(currentGeneration)

    def Evolve_For_One_Generation(self,currentGeneration):
        self.Spawn()
        self.Mutate()
        if currentGeneration == 0: 
            self.child.Evaluate("GUI")
        else:
            self.child.Evaluate("DIRECT")

        self.Print()
        self.Select()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)

    def Mutate(self):
        self.child.Mutate()

    def Select(self):
        if self.parent.fitness > self.child.fitness:
            self.parent = self.child

    def Print(self):
        print(self.parent.fitness,self.child.fitness)

    def Show_Best(self):
        # self.parent.Evaluate("GUI")
        pass


