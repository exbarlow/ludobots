import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER
from solution import SOLUTION
from datetime import datetime

# for _ in range(5):
#     os.system("python3 generate.py")
#     os.system("cat brain.nndf")
#     os.system("python3 simulate.py")
dummy = SOLUTION(-1)
dummy.Create_World()
dummy.Create_Body()
startTime = datetime.now()
print(f"Search starting at:",startTime.time())
phc = PARALLEL_HILL_CLIMBER()
phc.Evolve()
endTime = datetime.now()
print(f"Search finished at",endTime.time())
print(f"    duration:",str(endTime-startTime))
phc.Show_Best()