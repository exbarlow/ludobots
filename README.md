# ludobots assignment 5

### Environment Setup

All of the used modules can be found in `requirements.txt`. It is recommended to create a local environment (for example, using `python3 -m venv env`),
and installing the requirements locally with `pip3 -r requirements.txt`.

The experiment can be run with `python3 search.py {trial_name}`. 

There are two randomly generated bodies in the `saved_searches` folder, as well as two evolved bodies.

### New Functionalities (aside from each individual branch, which have their respective changes in their own `README.md`s)

- Saved Searches
  - The best `brain.nndf` file corresponding to the "most fit" individual each run of `search.py` is automatically saved to `saved_searches/brain_{trial_name}.nndf`. Running `python3 viewSavedSearches.py` will run a simulation of each of these saved files on GUI mode. The corresponding `fitness_{trial_name}.txt` file is also saved to the same folder.
- New robot!
  - originally I wanted to give my robot wings and have it try to slow down its fall, after many hours of effort I realized pybullet has no air resistance!
  - now the robot has wings but they help it bounce!
- Bouncy fitness function
  - The fitness function counts a bounce as the gap between two steps where the robot makes contact with the ground
  - A big bounce requires the robot to be airborne during at least 100 simulation steps (in a single bounce)
  - The fitness function sums up the time spent airborne during big bounces, selecting for the largest airtime.
  



