import numpy as np
from random import random

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
                    self.brain.weights[x, y] = np.random

            if random() <= MUTATION:
                self.brain.biases[x] = np.random

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
