import glob

from src import constants as c
from src import Start_Saved_Simulation
#todo: add comments
if __name__ == "__main__":
    brain_files = glob.glob(f"{c.savedPath}brain/*.nndf")
    brain_files.sort()
    for file in brain_files:
        savedName = file.split('/')[2].replace('.nndf','')
        Start_Saved_Simulation(savedName)

