# ludobots assignment 5

### Environment Setup

All of the used modules can be found in `requirements.txt`. It is recommended to create a local environment (for example, using `python3 -m venv env`),
and installing the requirements locally with `pip3 -r requirements.txt`.

The experiment can be run with `python3 search.py {trial_name}`. 

### Branch Functionality

- Saved Searches
  - The best `brain.nndf` file corresponding to the "most fit" individual each run of `search.py` is automatically saved to `saved_searches/brain_{trial_name}.nndf`. Running `python3 viewSavedSearches.py` will run a simulation of each of these saved files on GUI mode. The corresponding `fitness_{trial_name}.txt` file is also saved to the same folder.
- Marching To The Beat
  - This branch has the same fitness function as the original quadruped. However, the Sense() function has been modified to match the "Marching to the Beat" sample project from the reddit thread. There are 3 saved searches of each of 3 different magnitudes of sin(x) (1x, 4x, 10x)in the `saved_searches/` folder.


