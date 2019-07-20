import gui
from train import *

NAME = "PongClub"
NUMBER_OF_AI = 2  # between 0 and 2
NUMBER_OF_GEN = 16
FROM_GEN = 16


TRAINING = 0
PLAYING = 1
AGAINST_BEST = 2
action = AGAINST_BEST
play_against = 32

if action == TRAINING:
    train(num_of_games=NUMBER_OF_GEN, from_num=FROM_GEN)
elif action == PLAYING:
    gui.game(NAME, NUMBER_OF_AI)
elif action == AGAINST_BEST:
    print("Playing against population " + str(play_against))
    population = read_population_num(play_against)

    print("selecting best player...")
    get_best(population)
    best = population.agents[0]

    print("starting")
    gui.game(NAME, 1, best)
