import gui
from train import *
from os import listdir
from os.path import isfile, join

NAME = "PongClub"
NUMBER_OF_AI = 2  # between 0 and 2
NUMBER_OF_GEN = 8


TRAINING = 0
PLAYING = 1
AGAINST_BEST = 2
action = TRAINING

if action == TRAINING:
    train(num_of_games=NUMBER_OF_GEN, from_num=8)
elif action == PLAYING:
    gui.game(NAME, NUMBER_OF_AI)
elif action == AGAINST_BEST:
    saved_pop = [f for f in listdir(DATA_DIR) if isfile(join(DATA_DIR, f))]
    saved_pop.sort()

    print("playing against " + saved_pop[-1])

    population = read_population(saved_pop[-1])
    get_best(population)
    best = population.agents[0]

    print("starting")
    gui.game(NAME, 1, best)
