from simulation import SIMULATION
import sys

if len(sys.argv) != 3:
    print("ERROR, two parameters should be passed in: the mode (either DIRECT or GUI) and the solution ID")
    exit()

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]
simulation = SIMULATION(directOrGUI,solutionID)
simulation.Run()
simulation.Get_Fitness()

