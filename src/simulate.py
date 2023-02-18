from src.simulation import SIMULATION
import sys

def simulate(directOrGUI,solutionID):
    simulation = SIMULATION(directOrGUI,solutionID)
    simulation.Run()
    simulation.Get_Fitness()

if __name__ == "__main__":
    directOrGUI = sys.argv[1]
    solutionID = sys.argv[2]  
    simulate(directOrGUI,solutionID)  

