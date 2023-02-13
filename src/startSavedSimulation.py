from datetime import datetime
from simulation import SIMULATION

def Start_Saved_Simulation(savedName:str):
    """
    Runs a simulation of the given brain file.

    @savedName: The name of the saved simulation to run.

    @return: None
    """
    startTime = datetime.now()
    print(f"Started simulation of {savedName} at:",startTime.time())
    simulation = SIMULATION("GUI",-1,savedName)
    simulation.Run(savedName)
    endTime = datetime.now()
    print(f"Finished simulation of {savedName} at:",endTime.time())
    print(f"    duration:",str(endTime-startTime))