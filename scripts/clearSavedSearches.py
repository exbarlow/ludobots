import os
import sys
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../src'))
import constants as c

def Clear_Saved_Searches():
    """
    Clears the brain and fitness files from the saved_searches folder.

    @return: None
    """
    os.system(f"rm -v {c.savedPath}brain/*")
    os.system(f"rm -v {c.savedPath}fitness/*")

if __name__ == "__main__":
    Clear_Saved_Searches()
