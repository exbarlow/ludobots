# Artificial Life Final Project -- The Engineer

## Teaser Gif (sorry for low quality)
![name](readme_media/10_second_teaser.mp4)

## Environment Setup

All of the used modules can be found in `requirements.txt`. It is recommended to create a local environment (for example, using `python3 -m venv env`),
and installing the requirements locally with `pip3 -r requirements.txt`. I ran this on python 3.11, though I don't think there should be any problems using 3.10 or 3.9.

## 2-minute video
- [ ] Upload 2-minute video link

## Methods
Below are the run instrunctions, as well a diagram explaining the program flow through the different files of this repository, as well as diagrams explaining brain & body generation and representation, mutation, and evolution throughout the generations.

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
![mutation_diagram](readme_media/mutation_diagram.jpg)
![evolution_diagram](readme_media/evolution_diagram.jpg)

## Results
- [ ] Include a geneaology video (maybe a sequence of screenshots, show a couple moving).
- [ ] Include the 500 trial
  - there is a kind of elbow in the graph around ~40/50th trial, then huge amounts of flat space, occasionally raising slightly.
- [ ] Write some explanation about how they get stuck
- [ ] Include here two genealogies (as gifs & graph)
- Something else that I was interested in was the effect of the shape of the robot's neural net (which I held constant) on the shape of the max_fitness curve. So, I ran an abbreviated simulation comparing small-net (4,2,) -- the same used in the above trial, with large-net (16,8,4). Both simulations ran with population size 10, for 200 generations, and were run 10 separate times. The graphs are presented below.
- ![small-net](readme_media/small-net.png)
- ![large-net](readme_media/large-net.png)
- Something that instantly jumped out to me was how with the smaller net, the vast majority of the improvement via mutation ocurred within the first 100 generations, whereas with the larger net, many of the trials improved throughout the run, with very few having extremely long flat segments of no improvement. At first glance this makes sense, that a larger neural net would improve for longer as it has a much larger search space, but what is interesting about this is that the neural net only controls how the robot moves in response its sensors, and doesn't control as directly how the model decides what a "good" robot is. I don't fully understand why the larger net robots don't get stuck in local maxima for as long as the small-net robots do. Perhaps it would be interesting to run the comparison for more generations to see if this increasing trend continues, and for how long. It is also possible that this sample is due to a small sample size.
- Here are some statistics related to the above comparison:
- [ ] Include statistics.
- As seen in the above graphs, there are often periods of long stagnation in evolution. This is expected with a hill climber-based evolutionary algorithm, as no change in the organism will occur if there was no beneficial mutation. Mutations do not occur every cycle (see 
- In the future it would be interesting to compare the currently used evolutionary algorithm, which stifles genetic diversity but allows for more opportunities for one individual solution to escape a local max, with evolutionary algorithms that do not use hill-climbing, allowing for temporary dips in fitness, as well as with algorithms that allow for a greater amount of diversity.


### Citation
this project was inspired by https://www.reddit.com/r/ludobots/
and builds upon the following pyrosim repo: https://github.com/jbongard/pyrosim
