import random

# Local modules
from game import PLAYER_1, PLAYER_2


MAX_SPEED = 400
BALL_W = BALL_H = 20
MOMENTUM = 0.15


class Ball:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.dx = random.uniform(-MAX_SPEED, MAX_SPEED)
        self.dy = random.uniform(-MAX_SPEED / 3, MAX_SPEED / 3)
        self.width = width
        self.height = height
        self.left = self.x
        self.right = self.x + BALL_W
        self.top = self.y + BALL_H
        self.bottom = self.y

    def reset_bounds(self):
        self.left = self.x
        self.right = self.x + BALL_W
        self.top = self.y + BALL_H
        self.bottom = self.y

    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.reset_bounds()

    def collides(self, paddle):
        # check horizontal
        if self.left > paddle.right or self.right < paddle.left:
            return False
        # check vertical
        if self.bottom > paddle.top or self.top < paddle.bottom:
            return False
        return True

    def reset(self, serve=None):
        self.x = (self.width - BALL_W) / 2
        self.y = (self.height - BALL_H) / 2
        if not serve:
            self.dx = random.uniform(0.3 * MAX_SPEED, MAX_SPEED)
            if random.random() < 0.5:
                self.dx = -self.dx
        elif serve == PLAYER_1:
            self.dx = random.uniform(MAX_SPEED * 0.3, MAX_SPEED)
        else:
            self.dx = random.uniform(-MAX_SPEED, -0.3 * MAX_SPEED)
        self.dy = random.uniform(-MAX_SPEED / 3, MAX_SPEED / 3)
        self.reset_bounds()

    def horizontal_bounce(self):
        self.dx = -self.dx * (1 + MOMENTUM)
        if self.dy < 0:
            self.dy = random.uniform(-MAX_SPEED, 0)
        else:
            self.dy = random.uniform(0, MAX_SPEED)
