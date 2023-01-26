import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER

# for _ in range(5):
#     os.system("python3 generate.py")
#     os.system("cat brain.nndf")
#     os.system("python3 simulate.py")

phc = PARALLEL_HILL_CLIMBER()
phc.Evolve()
phc.Show_Best()