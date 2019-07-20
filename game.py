import pygame
from ai import *

BALL_RADIUS = 10
BALL_COLOR = (230, 230, 240)
BALL_INITIAL_SPEED = 20
BALL_MAX_SPEED = 25

PLAYER_SIZE = (20, 100)
PLAYER_COLOR = BALL_COLOR
PLAYER_VELOCITY = 40

VELOCITY_PASS_COEF = 0.5


class Game(object):
    def __init__(self, win_size, number_of_ai, first_agent=None, second_agent=None):
        self.ball = Ball(win_size)
        self.player1 = Player(True, win_size, ai=number_of_ai > 0, agent=first_agent)
        self.player2 = Player(False, win_size, ai=number_of_ai > 1, agent=second_agent)
        self.number_of_ai = number_of_ai
        self.win_size = win_size
        self.score = (0, 0)
        self.playing = True

    def step(self):
        self.player1.step(self.ball, self.player2)
        self.player2.step(self.ball, self.player1)
        val = self.ball.update(self.player1, self.player2)

        if val < 0:
            self.score = (self.score[0], self.score[1] + 1)
            self.reset()
        elif val > 0:
            self.score = (self.score[0] + 1, self.score[1])
            self.reset()

        if self.score[0] > 10 or self.score[1] > 10:
            self.playing = False

    def reset(self):
        self.ball.reset(self.win_size)
        self.player1.reset(self.win_size)
        self.player2.reset(self.win_size)

    def draw(self, window):
        self.player1.draw(window)
        self.player2.draw(window)
        self.ball.draw(window)


class Ball(object):
    def __init__(self, win_size):
        self.velocity = (BALL_INITIAL_SPEED, 0)
        self.position = (win_size[0] / 2, win_size[1] / 2)
        self.win_size = win_size

    def reset(self, win_size):
        self.velocity = (BALL_INITIAL_SPEED, 0)
        self.position = (win_size[0] / 2, win_size[1] / 2)
        self.win_size = win_size

    def pos_to_int(self):
        return int(self.position[0]), int(self.position[1])

    def draw(self, window):
        pygame.draw.circle(window, BALL_COLOR, self.pos_to_int(), BALL_RADIUS)

    def update(self, player1, player2):
        self.check_collision_with_player(player1)
        self.check_collision_with_player(player2)

        val = 0

        if self.position[0] - BALL_RADIUS < 0:
            # self.position = (-self.position[0], self.position[1])
            self.velocity = (-self.velocity[0], self.velocity[1])
            val = -1
        elif self.position[0] + BALL_RADIUS >= self.win_size[0]:
            # self.position = (2 * self.win_size[0] - self.position[0] - BALL_RADIUS, self.position[1])
            self.velocity = (-self.velocity[0], self.velocity[1])
            val = 1

        if self.position[1] - BALL_RADIUS < 0:
            # self.position = (self.position[0], -self.position[1])
            self.velocity = (self.velocity[0], -self.velocity[1])
        elif self.position[1] + BALL_RADIUS >= self.win_size[1]:
            # self.position = (self.position[0], 2 * self.win_size[1] - self.position[1] - BALL_RADIUS)
            self.velocity = (self.velocity[0], -self.velocity[1])

        self.position = (
            self.position[0] + self.velocity[0],
            self.position[1] + self.velocity[1]
        )

        return val

    def check_collision_with_player(self, player):
        vel_x, vel_y = self.velocity

        if player.left:
            if self.position[0] - BALL_RADIUS <= PLAYER_SIZE[0] and \
                    player.position[1] <= self.position[1] <= player.position[1] + PLAYER_SIZE[1]:
                vel_x = abs(vel_x)
                # vel_y += player.velocity[1] * VELOCITY_PASS_COEF
                if self.position[1] <= player.position[1] + PLAYER_SIZE[1]/2:
                    vel_y -= PLAYER_VELOCITY
                else:
                    vel_y += PLAYER_VELOCITY
        else:
            if self.position[0] + BALL_RADIUS >= self.win_size[0] - PLAYER_SIZE[0] and \
                    player.position[1] <= self.position[1] <= player.position[1] + PLAYER_SIZE[1]:
                vel_x = -abs(vel_x)
                # vel_y -= player.velocity[1] * VELOCITY_PASS_COEF
                if self.position[1] <= player.position[1] + PLAYER_SIZE[1]/2:
                    vel_y -= PLAYER_VELOCITY
                else:
                    vel_y += PLAYER_VELOCITY

        if vel_x < -BALL_MAX_SPEED:
                vel_x = -BALL_MAX_SPEED
        elif vel_x > BALL_MAX_SPEED:
            vel_x = BALL_MAX_SPEED
        if vel_y < -BALL_MAX_SPEED:
            vel_y = -BALL_MAX_SPEED
        elif vel_y > BALL_MAX_SPEED:
            vel_y = BALL_MAX_SPEED

        self.velocity = (vel_x, vel_y)


class Player(object):
    def __init__(self, left, win_size, ai=False, agent=None):
        self.velocity = (0, PLAYER_VELOCITY)
        self.position = (
            0 if left else win_size[0] - PLAYER_SIZE[0],
            (win_size[1] - PLAYER_SIZE[1]) / 2
        )
        self.left = left
        self.ai = ai
        self.win_size = win_size

        if self.ai and agent:
            self.agent = agent
        elif self.ai:
            self.agent = AIPlayer()

    def reset(self, win_size):
        self.velocity = (0, PLAYER_VELOCITY)
        self.position = (
            0 if self.left else win_size[0] - PLAYER_SIZE[0],
            (win_size[1] - PLAYER_SIZE[1]) / 2
        )
        self.win_size = win_size

    def draw(self, window):
        pygame.draw.rect(window, PLAYER_COLOR, (self.position[0], self.position[1], PLAYER_SIZE[0], PLAYER_SIZE[1]))

    def step(self, ball, enemy):
        if self.ai:
            action = self.agent.get_action(ball, self, enemy)
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                action = 0
            elif keys[pygame.K_DOWN]:
                action = 1
            else:
                action = -1

        if action == 0:
            self.move(True)
            self.velocity = (0, -PLAYER_VELOCITY)
        elif action == 1:
            self.move(False)
            self.velocity = (0, PLAYER_VELOCITY)
        else:
            self.velocity = (0, 0)

        self.update()

    def update(self):
        if self.position[0] < 0:
            self.position = (
                0,
                self.position[1]
            )
            self.velocity = (
                0,
                self.velocity[1]
            )
        elif self.position[0] + PLAYER_SIZE[0] > self.win_size[0]:
            self.position = (
                self.win_size[0] - PLAYER_SIZE[0],
                self.position[1]
            )
            self.velocity = (
                0,
                self.velocity[1]
            )
        if self.position[1] < 0:
            self.position = (
                self.position[0],
                0
            )
            self.velocity = (
                self.velocity[0],
                0
            )
        elif self.position[1] + PLAYER_SIZE[1] > self.win_size[1]:
            self.position = (
                self.position[0],
                self.win_size[1] - PLAYER_SIZE[1],
            )
            self.velocity = (
                self.velocity[0],
                0
            )

    def move(self, up):
        self.position = (
            self.position[0],
            self.position[1] + PLAYER_VELOCITY * (-1 if up else 1)
        )
