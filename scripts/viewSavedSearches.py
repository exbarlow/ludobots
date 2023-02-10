import glob
import sys
import os
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../src'))
from datetime import datetime
import constants as c
from simulation import SIMULATION

def Start_Saved_Simulation(nndfName:str):
    """
    Runs a simulation of the given brain file.

    @nndfName: The name of the brain file to simulate.

    @return: None
    """
    startTime = datetime.now()
    print(f"Started simulation of {nndfName} at:",startTime.time())
    simulation = SIMULATION("GUI",-1,nndfName)
    simulation.Run(nndfName)
    endTime = datetime.now()
    print(f"Finished simulation of {nndfName} at:",endTime.time())
    print(f"    duration:",str(endTime-startTime))

if __name__ == "__main__":
    brain_files = glob.glob(f"{c.savedPath}brain/*.nndf")
    for file in brain_files:
        savedName = file.split('/')[2].replace('.nndf','')
        #! temp
        print(savedName)
        Start_Saved_Simulation(savedName)

