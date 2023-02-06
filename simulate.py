from simulation import SIMULATION
from solution import SOLUTION
import sys

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]

simulation = SIMULATION(directOrGUI,solutionID)
simulation.Run()
simulation.Get_Fitness()

