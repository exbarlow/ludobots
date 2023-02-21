# Artificial Life Assignment 7

### Environment Setup

All of the used modules can be found in `requirements.txt`. It is recommended to create a local environment (for example, using `python3 -m venv env`),
and installing the requirements locally with `pip3 -r requirements.txt`.

### New Functionalities since Assignment 6

- Repository refactoring
  - Scripts need to be run as modules now.
    - `python3 -m scripts.search {name}` runs a search and saves the best result to `saved_searches/` under the name of `name`.
    - `python3 -m scripts.runner` runs multiple searches.
    - `python3 -m scripts.viewSaved` plays all of the simulations saved to `saved_searches/`.
    - `python3 -m scripts.clearSaved` clears the `saved_searches/` directory.
- Fitness function change
  - now, maximizing distance traveled in the y direction. This was really just to get them to move for the video. Again, there is no evolution as each generation is randomly generated, but this is what was used to get moving simulations for the video.

- 8 example searches
  - in `saved_searches/` there are 8 saved trials. 4 are `dynamic` and involve movement of randomly generated bodies with all joints set to type `"revolute"`. 4 are `fixed` and involve still randomly generated bodies will all joints set to type `"fixed"`, in order to show the phenotype better before it is distorted by the hinge joints.
  
- 3D Expansion:
  - number of links and proportion of links to receive sensors is specified in `src/constants.py` as before. See diagram below for generation.
  - note that joint axes were randomly selected from either of the axes orthogonal to the joint's direction vector (from the face of the parent)
  ![generation diagram](diagram.jpg)
  


Inspired by https://www.reddit.com/r/ludobots/
