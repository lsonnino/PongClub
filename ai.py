import numpy as np
from random import random, randint

INPUTS = 6
OUTPUTS = 2

MUTATION = 0.1


class NeuralNetwork(object):
    def __init__(self):
        self.weights = np.zeros((OUTPUTS, INPUTS))
        self.biases = np.zeros(OUTPUTS)

        self.initialize()

    def initialize(self):
        for x in range(OUTPUTS):
            for y in range(INPUTS):
                self.weights[x, y] = 2 * random() - 1

            self.biases[x] = 2 * random() - 1

    def clone(self):
        new = NeuralNetwork()

        new.weights = np.copy(self.weights)
        new.biases = np.copy(self.biases)

        return new

    def forward(self, input):
        ouput = np.zeros(OUTPUTS)

        for o in range(OUTPUTS):
            ouput[o] = np.dot(input, self.weights[o]) + self.biases[o]

        return ouput


class AIPlayer(object):
    def __init__(self):
        self.brain = NeuralNetwork()

    def mutate(self):
        for x in range(OUTPUTS):
            for y in range(INPUTS):
                if random() <= MUTATION:
                    self.brain.weights[x, y] = 2 * random() - 1

            if random() <= MUTATION:
                self.brain.biases[x] = 2 * random() - 1

    def get_action(self, ball, player, enemy):
        input = np.zeros(INPUTS)

        input[0] = player.position[1]
        input[1] = enemy.position[1]

        input[2] = ball.position[0]
        input[3] = ball.position[1]
        input[4] = ball.velocity[0]
        input[5] = ball.velocity[1]

        output = self.brain.forward(input)

        max = -1
        val = -1
        for o in range(OUTPUTS):
            if max < 0 or val < output[o]:
                max = o
                val = output[o]

        return max

    def clone(self):
        agent = AIPlayer()
        agent.brain = self.brain.clone()

        return agent


class Population(object):
    def __init__(self, size):
        self.agents = []
        for i in range(size):
            self.agents.append(AIPlayer())
        self.splits = []
        self.rest = None

    def split(self):
        remaining = []
        for i in range(len(self.agents)):
            remaining.append(self.agents[i].clone())

        self.splits = []
        while len(remaining) > 1:
            first = randint(0, len(remaining) - 1)
            second = randint(0, len(remaining) - 2)

            agent_first = remaining[first].clone()
            remaining.remove(remaining[first])
            agent_second = remaining[second].clone()
            remaining.remove(remaining[second])

            self.splits.append((agent_first.clone(), agent_second.clone()))

        if len(remaining) == 1:
            self.rest = remaining[0]
        else:
            self.rest = None

    def mutate(self, results):
        for i in range(len(results)):
            winner = self.splits[i][1 if results[i] else 0]

            self.splits[i] = (winner.clone(), winner.clone())
            self.splits[i][0].mutate()
            self.splits[i][1].mutate()

    def fetch(self):
        self.agents = []
        for i in range(len(self.splits)):
            self.agents.append(self.splits[i][0])
            self.agents.append(self.splits[i][1])

        if self.rest:
            self.agents.append(self.rest)
