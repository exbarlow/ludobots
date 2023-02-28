import sys
from datetime import datetime

from src import PARALLEL_HILL_CLIMBER
from src import Create_World

def search(saveName,toGraph):
    """
    Runs a search for the most fit individual, based on parameters set in the constants.py file.
    
    @saveName: The name of the file to save the best solution to.

    @return: None
    """
    Create_World()
    startTime = datetime.now()
    print(f"Search starting at:",startTime.time())
    phc = PARALLEL_HILL_CLIMBER(toGraph == "True",saveName=saveName)
    phc.Evolve()
    endTime = datetime.now()
    print(f"Search finished at",endTime.time())
    print(f"    duration:",str(endTime-startTime))
    phc.Show_Best(saveName)

if __name__ == "__main__":
    if len(sys.argv) == 0:
        print("Please provide a save name for the best solution.")
        exit()
    elif len(sys.argv) > 3:
        print("Please provide only two arguments -- the save name for the best solution & whether or not it should be graphed.")
        exit()
    search(sys.argv[1],sys.argv[2])