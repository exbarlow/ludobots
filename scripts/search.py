import sys
import os
# sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../src'))
from src.parallelHillClimber import PARALLEL_HILL_CLIMBER
from datetime import datetime
from src.utils import Create_World

def search(saveName):
    """
    Runs a search for the most fit individual, based on parameters set in the constants.py file.
    
    @saveName: The name of the file to save the best solution to.

    @return: None
    """
    Create_World()
    startTime = datetime.now()
    print(f"Search starting at:",startTime.time())
    phc = PARALLEL_HILL_CLIMBER()
    phc.Evolve()
    endTime = datetime.now()
    print(f"Search finished at",endTime.time())
    print(f"    duration:",str(endTime-startTime))
    phc.Show_Best(saveName)

if __name__ == "__main__":
    if len(sys.argv) == 0:
        print("Please provide a save name for the best solution.")
        exit()
    elif len(sys.argv) > 2:
        print("Please provide only one argument -- the save name for the best solution.")
        exit()
    search(sys.argv[1])