import os

def runner(numTrials):
    """
    Runs the search.py script numTrials times.

    @numTrials: The number of times to run the search.py script.

    @return: None
    """
    for i in range(numTrials):
        os.system(f"python3 scripts/search.py trial{i}")

if __name__ == "__main__":
    runner(3)
