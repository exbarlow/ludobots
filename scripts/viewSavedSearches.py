import glob
import sys
import os
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../src'))
import constants as c
from startSavedSimulation import Start_Saved_Simulation

if __name__ == "__main__":
    brain_files = glob.glob(f"{c.savedPath}brain/*.nndf")
    for file in brain_files:
        savedName = file.split('/')[2].replace('.nndf','')
        Start_Saved_Simulation(savedName)

