import matplotlib.pyplot as plt

def read_data(name_pattern:str,num_trials:int):
    '''
    Reads in the maximum fitness for each generation for each trial in the run.

    @name_pattern: string pattern to match the name of the files to read in
    @num_trials: the number of trials in the run

    @Returns: A list of lists. The outer list contains one list for each trial. The inner lists contain the maximum fitness for each generation.
    '''
    assert isinstance(name_pattern,str), f'`name_pattern` must be a string. Received: {name_pattern}'
    assert isinstance(num_trials,int), f'`numTrials` must be an integer. Received: {num_trials}'

    data = [[] for _ in range(num_trials)]
    for i in range(num_trials):
        with open(f"evolutions/{name_pattern}/{i}.txt","r") as f:
            for line in f:
                data[i].append(float(line))

    return data

def plot(name_pattern:str,num_trials:int,xlabel:str='Generation',ylabel:str='Maximum Fitness Value',title:str='Fitness Value vs. Generation'):
    '''
    Plots the maximum fitness for each generation for each trial in the run, saving the graph to a file.

    @name_pattern: string pattern to match the name of the files to read in
    @num_trials: the number of trials in the run

    @Returns: None
    '''
    assert isinstance(name_pattern,str), f'`name_pattern` must be a string. Received: {name_pattern}'
    assert isinstance(num_trials,int), f'`numTrials` must be an integer. Received: {num_trials}'
    assert isinstance(xlabel,str), f'`xlabel` must be a string. Received: {xlabel}'
    assert isinstance(ylabel,str), f'`ylabel` must be a string. Received: {ylabel}'
    assert isinstance(title,str), f'`title` must be a string. Received: {title}'

    data = read_data(name_pattern,num_trials)
    for j in range(num_trials):
        plt.plot(data[j], label=f'{j}')
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    # plt.legend()
    plt.savefig(f"evolutions/{name_pattern}/{name_pattern}.png")
    plt.close()

if __name__ == "__main__":
    plot('large-net',10,title="Fitness Value vs. Generation -- Large Net")
    plot('cull-bottom-two',10,title="Fitness Value vs. Generation -- Small Net")