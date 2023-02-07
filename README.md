# ludobots assignment 5

### Environment Setup

All of the used modules can be found in `requirements.txt`. It is recommended to create a local environment (for example, using `python3 -m venv env`),
and installing the requirements locally with `pip3 -r requirements.txt`.

### Branch Structure

I experimented with a couple of the final project ideas in the reddit thread, they can be found in each of the branches below:
- Up up and Away (this branch!)
- Marching to the beat (marchingToTheBeat)

In each of these branches, the experiment can be run with `python3 search.py {trial_name}`. 

### New Functionalities (aside from each individual branch, which have their respective changes in their own `README.md`s)

- Saved Searches
  - The best `brain.nndf` file corresponding to the "most fit" individual each run of `search.py` is automatically saved to `saved_searches/brain_{trial_name}.nndf`. Running `python3 viewSavedSearches.py` will run a simulation of each of these saved files on GUI mode. The corresponding `fitness_{trial_name}.txt` file is also saved to the same folder.
- Up up and Away
  - This branch has had the fitness function modified to match the "up up and away" sample project from the reddit thread. There are 3 saved searches in the `saved_searches/` folder.


