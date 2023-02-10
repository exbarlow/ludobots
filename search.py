import sys
from parallelHillClimber import PARALLEL_HILL_CLIMBER
from solution import SOLUTION
from datetime import datetime

saveName = sys.argv[1]

dummy = SOLUTION(-1)
dummy.Create_World()
dummy.Create_Body(save=True)
startTime = datetime.now()
print(f"Search starting at:",startTime.time())
phc = PARALLEL_HILL_CLIMBER()
phc.Evolve()
endTime = datetime.now()
print(f"Search finished at",endTime.time())
print(f"    duration:",str(endTime-startTime))
phc.Show_Best(saveName)