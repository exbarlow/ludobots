# ludobots assignment 5

### Environment Setup

All of the used modules can be found in `requirements.txt`. It is recommended to create a local environment (for example, using `python3 -m venv env`),
and installing the requirements locally with `pip3 -r requirements.txt`.

### Branch Structure

I experimented with a couple of the final project ideas in the reddit thread, they can be found in each of the branches below:


In each of these branches, the experiment can be run with `python3 search.py`. Note that in the `Wait_For_Simulation_To_End` method within `solution.py`,
the values of `time.sleep()` are set very high to account for the fact that with my m1 chip, lower values cause synchronization issues. If this is 
not a problem for your machine, it is recommended to reduce these values to improve performance speed.

### New Functionalities (aside from each individual branch, which have their respective changes in their own `README.md`s)

- Saved Searches
  - The best `brain.nndf` file corresponding to the "most fit" individual each run of `search.py` is automatically saved to `saved_searches/`. Running `python3 viewSavedSearches.py` will run a simulation of each of these saved files on GUI mode.


