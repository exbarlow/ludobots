from simulation import SIMULATION
import sys

if len(sys.argv) != 2:
    print("ERROR, one and only one parameter should be passed in")
    exit()

directOrGUI = sys.argv[1]
simulation = SIMULATION(directOrGUI)
simulation.Run()
simulation.Get_Fitness()

