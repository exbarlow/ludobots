from solution import SOLUTION
import constants as c
import copy
import os
import time
class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("rm src/tempfiles/fitness/*.txt")
        os.system("rm src/tempfiles/brain/*.nndf")
        self.parents = {}
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(i)
        
    def Evaluate(self,solutions):
        for individual in solutions.values():
            individual.Start_Simulation("DIRECT")

        for individual in solutions.values():
            individual.Wait_For_Simulation_To_End()

    def Evolve(self):
        self.Evaluate(self.parents)

        for currentGeneration in range(c.numberOfGenerations):
            if currentGeneration%10 == 0:
                print("current generation:",currentGeneration)
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate(self.children)
        self.Evaluate(self.children)
        self.Select()
        self.Cull_And_Replace()
        self.Reassign_IDs()
        # self.Print_Highest_Fitness()

    def Spawn(self):
        self.children = {}
        for parentID, parent in self.parents.items():
            self.children[parentID] = copy.deepcopy(parent)

    def Mutate(self,solutions):
        for solution in solutions.values():
            solution.Mutate()

    def Select(self):
        for parentID, parent in self.parents.items():
            if parent.fitness < self.children[parentID].fitness:
                self.parents[parentID] = self.children[parentID]
    
    def Cull_And_Replace(self):
        parentsList = sorted(self.parents.items(), key=lambda x: x[1], reverse=True)
        self.parents = {ind: v[1] for ind, v in enumerate(parentsList[:c.populationSize//c.cullSize])}
        clones = []

        for _ in range(c.cullSize-1):
            for parent in self.parents.values():
                clones.append(copy.deepcopy(parent))

        while len(clones) + len(self.parents) < c.populationSize:
            clones.append(copy.deepcopy(parentsList[0][1]))

        for ind, clone in enumerate(clones):
            self.parents[c.populationSize//c.cullSize + ind] = clone

    def Reassign_IDs(self):
        for parentID in self.parents:
            self.parents[parentID].myID = parentID

    def Print_Highest_Fitness(self):
        bestParent = max(self.parents.values())
        print(bestParent.fitness)

    def Show_Best(self,saveName):
        bestParent = max(self.parents.values())
        self.Print_Highest_Fitness()
        bestParent.Start_Simulation("GUI",save=True)

        i = 0
        foundFitness = True
        while not os.path.exists(f"src/tempfiles/fitness/{bestParent.myID}.txt"):
            time.sleep(0.25)
            i += 0.25
            if i > 5:
                foundFitness = False
                break

        if foundFitness:
            os.system(f"mv src/tempfiles/fitness/{bestParent.myID}.txt {c.savedPath}fitness/{saveName}.txt")
        os.system(f"mv {c.savedPath}brain/{bestParent.myID}.nndf {c.savedPath}brain/{saveName}.nndf")



