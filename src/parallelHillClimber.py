from solution import SOLUTION
import constants as c
import copy
import os
import time
class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system(f"rm {c.tempfilePath}fitness/*.txt")
        os.system(f"rm {c.tempfilePath}brain/*.nndf")
        os.system(f"rm {c.tempfilePath}body/*.urdf")
        self.parents = {}
        for i in range(c.populationSize):
            self.parents[i] = SOLUTION(i)
        
    def Evaluate(self,solutions):
        """
        Evaluates the fitness of each solution in the solutions dictionary.

        @solutions: A dictionary of solutions to evaluate. Usually self.parents or self.children.

        @return: None
        """
        for individual in solutions.values():
            individual.Start_Simulation("DIRECT")

        for individual in solutions.values():
            individual.Wait_For_Simulation_To_End()

    def Evolve(self):
        """
        Evaluate parents, then evolves for numberOfGenerations generations.

        @return: None
        """
        self.Evaluate(self.parents)

        for currentGeneration in range(c.numberOfGenerations):
            if currentGeneration%10 == 0:
                print("current generation:",currentGeneration)
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        """
        Evolves the population for one generation.

        @return: None
        """
        self.Spawn()
        self.Mutate(self.children)
        self.Evaluate(self.children)
        self.Select()
        self.Cull_And_Replace()
        self.Reassign_IDs()
        # self.Print_Highest_Fitness()

    def Spawn(self):
        """
        Creates a copy of each parent and stores it in self.children.

        @return: None
        """
        self.children = {}
        for parentID, parent in self.parents.items():
            self.children[parentID] = copy.deepcopy(parent)

    def Mutate(self,solutions):
        """
        Mutates each solution in the solutions dictionary.

        @solutions: A dictionary of solutions to mutate. Usually self.children.
        """
        for solution in solutions.values():
            solution.Mutate()

    def Select(self):
        """
        Selects between parent and child for each parent, replacing parent with its child if its fitness is higher. 

        @return: None
        """
        for parentID, parent in self.parents.items():
            if parent.fitness < self.children[parentID].fitness:
                self.parents[parentID] = self.children[parentID]
    
    def Cull_And_Replace(self):
        """
        Selects a percentage of the population to keep, then replaces the rest with clones of the kept percentage. Percentage is determined by constants.cullSize.

        @return: None
        """
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
        """
        Reassigns the myID attribute of each parent to its key in self.parents in order to keep the range of ids [0,constants.populationSize).

        @return: None
        """
        for parentID in self.parents:
            self.parents[parentID].myID = parentID

    def Print_Highest_Fitness(self,reverse=False):
        """
        Prints the fitness of the most fit parent.

        @reverse: If True, prints the fitness of the parent with smallest fitness (for cases where fitness should be minimized).

        @return: None
        """
        bestParent = max(self.parents.values())
        if reverse:
            print(-1 * bestParent.fitness)
        else:
            print(bestParent.fitness)

    def Show_Best(self,saveName):
        """
        Runs the simulation of the most fit parent, then saves the fitness and brain files to saved_searches/fitness and saved_searches/brain respectively.

        @saveName: The name to save the fitness file as. Should not include the file extension or directory structure.

        @return: None
        """
        bestParent = max(self.parents.values())
        self.Print_Highest_Fitness()
        bestParent.Start_Simulation("DIRECT",save=False)
        # save fitness so that we can annotate it when the simulation is run in GUI mode
        bestParent.Wait_For_Simulation_To_End(save=True)

        i = 0
        foundFitness = True
        while not os.path.exists(f"{c.savedPath}fitness/{bestParent.myID}.txt"):
            time.sleep(0.25)
            i += 0.25
            if i > 5:
                foundFitness = False
                break

        if foundFitness:
            bestParent.Start_Simulation("GUI",save=True)
            # don't save fitness this time because we already saved it
            bestParent.Wait_For_Simulation_To_End(save=False)

            # rename the saved files to the provided saveName
            os.system(f"mv {c.savedPath}fitness/{bestParent.myID}.txt {c.savedPath}fitness/{saveName}.txt")
            os.system(f"mv {c.savedPath}brain/{bestParent.myID}.nndf {c.savedPath}brain/{saveName}.nndf")
            os.system(f"mv {c.savedPath}body/{bestParent.myID}.urdf {c.savedPath}body/{saveName}.urdf")

        else:
            print("Error finding fitness file. TODO: test is this is m1 related.")
            os.system(f"rm {c.savedPath}brain/{bestParent.myID}.nndf")
            os.system(f"rm {c.savedPath}body/{bestParent.myID}.urdf")




