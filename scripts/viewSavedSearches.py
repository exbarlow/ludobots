import glob
from datetime import datetime
from ..src.constants import *
from ..src.simulation import SIMULATION

def Start_Saved_Simulation(nndfName:str):
    startTime = datetime.now()
    print(f"Started simulation of {nndfName} at:",startTime.time())
    simulation = SIMULATION("GUI",-1,nndfName)
    simulation.Run(nndfName)
    endTime = datetime.now()
    print(f"Finished simulation of {nndfName} at:",endTime.time())
    print(f"    duration:",str(endTime-startTime))

if __name__ == "__main__":
    brain_files = glob.glob(f"{savedPath}brain/*.nndf")
    for file in brain_files:
        Start_Saved_Simulation(file)

