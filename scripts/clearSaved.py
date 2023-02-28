import os

from src import constants as c

def Clear_Saved_Searches():
    """
    Clears the brain and fitness files from the saved_searches folder.

    @return: `None`
    """
    os.system(f"rm -v {c.savedPath}brain/*")
    os.system(f"rm -v {c.savedPath}fitness/*")
    os.system(f"rm -v {c.savedPath}body/*")

if __name__ == "__main__":
    Clear_Saved_Searches()
