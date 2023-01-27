import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER
from solution import SOLUTION

# for _ in range(5):
#     os.system("python3 generate.py")
#     os.system("cat brain.nndf")
#     os.system("python3 simulate.py")
dummy = SOLUTION(-1)
dummy.Create_World()
dummy.Create_Body()
phc = PARALLEL_HILL_CLIMBER()
phc.Evolve()
phc.Show_Best()