from datetime import datetime

import src.pyrosim.pyrosim as pyrosim
from src.simulation import SIMULATION

def Create_World():
    """
    Creates a world for the simulation. Currently, this is just a blank world.

    @return: None
    """
    pyrosim.Start_SDF("src/robotfiles/world.sdf")
    pyrosim.End()

def Start_Saved_Simulation(savedName:str):
    """
    Runs a simulation of the given brain file.

    @savedName: The name of the saved simulation to run.

    @return: None
    """
    startTime = datetime.now()
    print(f"Started simulation of {savedName} at:",startTime.time())
    simulation = SIMULATION("GUI",-1,savedName)
    simulation.Run()
    endTime = datetime.now()
    print(f"Finished simulation of {savedName} at:",endTime.time())
    print(f"    duration:",str(endTime-startTime))