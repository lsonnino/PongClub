from multiprocessing.pool import ThreadPool
from gui import WIN_SIZE
from game import *
import pickle
import os
import shutil

POPULATION_SIZE = 256
DATA_DIR = "populations"
POPULATION_EXTENSION = "pop"


def match(first, second):
    game = Game(WIN_SIZE, 2, first, second)

    while game.playing:
        game.step()

    return game.score[1] > game.score[0]


def do_match(matches):
    threads = []
    t_results = []
    m_results = []
    for m in matches:
        t = ThreadPool(processes=1)
        threads.append(t)
        t_results.append(t.apply_async(match, (m[0], m[1])))

    for i in range(len(t_results)):
        m_results.append(t_results[i].get())
        threads[i].close()
        threads[i].join()

    return m_results


def train(num_of_games=-1, from_num=-1):
    if from_num > 0:
        population = read_population_num(from_num)
    else:
        population = Population(POPULATION_SIZE)

        if os.path.exists(DATA_DIR):
            shutil.rmtree(DATA_DIR)
        os.mkdir(DATA_DIR)

    offset = from_num if from_num > 0 else 0

    gen = 1 + offset
    while gen <= num_of_games + offset:
        print("gen " + str(gen) + " out of " + str(num_of_games + offset))

        save_population_num(population, gen)

        population.split()

        population.mutate(do_match(population.splits))
        population.fetch()

        gen += 1


def get_best(population):
    while len(population.agents) > 1:
        print(str(len(population.agents)) + " left")

        population.split()

        res = do_match(population.splits)
        agents = []
        for i in range(len(res)):
            agents.append(population.splits[i][1 if res[i] else 0].clone())

        population.agents = agents


def read_population_num(num):
    return read_population(str(num) + '.' + POPULATION_EXTENSION)


def read_population(file_name):
    with open(DATA_DIR + '/' + file_name, 'rb') as f:
        return pickle.load(f)


def save_population_num(population, num):
    with open(DATA_DIR + '/' + str(num) + '.' + POPULATION_EXTENSION, 'wb') as f:
        pickle.dump(population, f)
