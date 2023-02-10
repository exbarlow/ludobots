import os
import sys
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../src'))
import constants as c

if __name__ == "__main__":
    os.system(f"rm -v {c.savedPath}brain/*")
    os.system(f"rm -v {c.savedPath}fitness/*")

