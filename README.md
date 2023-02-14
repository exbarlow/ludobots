# Artificial Life Assignment 6

### Environment Setup

All of the used modules can be found in `requirements.txt`. It is recommended to create a local environment (for example, using `python3 -m venv env`),
and installing the requirements locally with `pip3 -r requirements.txt`.

### New Functionalities since Assignment 5

- Repository refactoring
  - I moved most things into the `src/` folder and created new folders within that to hold temporary files.
  - `saved_searches/` now contains subfolders for the `body.urdf`, `brain.nndf`, and `fitness.txt` files of each saved run.
  - scripts were moved into the `scripts/` subfolder
    - this means that an individual trial can be run with `python3 scripts/search.py {save name}`
    - you can run `python3 scripts/runner.py` to run a bunch of trials and save them all (can edit this file)
    - you can run `python3 scripts/viewSavedSearches.py` to see all of the saved searches. Now the fitness of each best invidiual is printed to the screen!
    - you can run `python3 scripts/clearSavedSearches.py` to empty the `saved_searches/` folder
- Neural Network with hidden layers!
  - in `src/constants.py` you can specify the number of layers and number of hidden neurons within each layer.
  - Currently, all hidden layers are fully connected
- Evolution algorithm revamp
  - now, after being compared to each child, the best is selected, then, a certain proportion of the "winners" become parents for the next generation
  - the actual mutation was slightly altered to add or subtract a proportion of the affected weight
    - the chance this happens to any given rate is controlled by `mutationRate` in `src/constants.py`
    - the magnitude of this mutation is given by `mutationPower` in `src/constants.py`
  - none of this actually does anything, as the `body.urdf` files are re-randomized each generation so no evolution really happens, but the groundwork is set up for the future (and it took me a really long time)
- Snake creation! (the actual required part of this assignment)
  - each invidiual is created with a number of links between `minLinks` and `maxLinks` (inclusive) in `src/constants.py`
  - each link has its x, y, and z coordinates uniformly selected between `minLinkSize` and `maxLinkSize` in `src/constants.py`
  - a proportion of links to contain sensors is uniformly selected between `minSensorProportion` and `maxSensorProportion` in `src/constants.py`
    - this is rounded to an integer number of links (minimum 1)
    - the links selected to contain a sensor are colored green
- 4 example searches
  - in `saved_searches/` there are 4 saved trials. The fitness function is to maximize highest jump height, though there is no real evolution so these are just randomly selected as the best from independent random trials. My personal favorite is `dyanmic_trial1` because it's actually doing the worm.
  


