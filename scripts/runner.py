import os
import matplotlib.pyplot as plt
from src import constants as c

def runner(numTrials:int):
    """
    Runs the `search.py` script `numTrials` times.

    @param `numTrials`: The number of times to run the `search.py` script.

    @return: `None`
    """
    graph = numTrials == 5
    name = "plot_trial"
    for i in range(numTrials):
        # will add these to the graph
        
        os.system(f"python3 -m scripts.search {name}_{i} {graph}")

    if graph:
        data = [[] for _ in range(numTrials)]
        for i in range(numTrials):
            with open(f"scripts/{name}_{i}.txt","r") as f:
                for line in f:
                    data[i].append(float(line))

        # plot the lines
        for j in range(numTrials):
            fitness_values = data[j]
            plt.plot(fitness_values, label=f'{name}_{j}')

        # set the labels and title
        plt.xlabel('Generation')
        plt.ylabel('Maximum Fitness Value')
        plt.title('Fitness Value vs. Generation')
        # add the legend
        plt.legend()
        # show the plot
        plt.savefig(f"scripts/{name}.png")
        plt.show()

        for j in range(numTrials):
            os.system(f"rm scripts/{name}_{j}.txt")

if __name__ == "__main__":
    runner(5)
