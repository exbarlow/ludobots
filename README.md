# Artificial Life Final Project -- The Engineer

## Teaser Gif (sorry for low quality)
- [ ] Upload teaser gif

## Environment Setup

All of the used modules can be found in `requirements.txt`. It is recommended to create a local environment (for example, using `python3 -m venv env`),
and installing the requirements locally with `pip3 -r requirements.txt`. I ran this on python 3.11, though I don't think there should be any problems using 3.10 or 3.9.

## 2-minute video
- [ ] Upload 2-minute video link

## Methods
- [ ] Include written explanation

### Run instructions
  - Scripts need to be run as modules.
    - `python -m scripts.search {name}` runs a search and saves the best result to `saved_searches/` under the name of `name`.
    - `python -m scripts.runner` runs multiple searches. It saves the sequence of max fitness per generation to a `.txt` file in the folder `evolutions/`.
    - `python -m scripts.analysis` currently graphs the searches saved in `evolutions/`. There also exist functions to generate more analytic data, such as the average improvement for each beneficial mutation, total number of beneficial mutations, frequency, etc.
    - `python -m scripts.viewSaved` plays all of the simulations saved to `saved_searches/`.
    - `python -m scripts.clearSaved` clears the `saved_searches/` directory.
    
### Program flow
- [ ] Upload Program flow diagram
    
### Body/Brain Generation, Mutation, and Evolution
- [ ] Upload Body/Brain Generation
- [ ] Upload Mutation
- [ ] Upload Selection/Evolution

## Results
- [ ] Include a geneaology video (maybe a sequence of screenshots, show a couple moving).
- [ ] Include the 500 trial
  - there is a kind of elbow in the graph around ~40/50th trial, then huge amounts of flat space, occasionally raising slightly.
- [ ] Write some explanation about how they get stuck
- [ ] Include here two genealogies (as gifs & graph)
- [ ] Was interested to see if there was any effect of the small neural network here --> maybe a larger network would allow the robot to learn different behaviors?
  - [ ] Include the plots and tables
- [ ] Some things that would be interesting to try in the future -- run this comparison with more trials, to see if the larger net would continue to improve above 200 trials.
- [ ] Test different evolutionary algorithm that allows dips in fitness to try and escape local maxima -- also one that allows for more genetic diversity.


### Citation
this project was inspired by https://www.reddit.com/r/ludobots/
and builds upon the following pyrosim repo: https://github.com/jbongard/pyrosim
