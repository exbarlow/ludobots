import os
from hillclimber import HILL_CLIMBER

# for _ in range(5):
#     os.system("python3 generate.py")
#     os.system("cat brain.nndf")
#     os.system("python3 simulate.py")

hc = HILL_CLIMBER()
hc.Evolve()