import numpy as np


class Paddle:
    REC_W = 40
    REC_H = 120
    SPEED = 600

    def __init__(self, x, y, limit):
        self.x = x
        self.y = y
        self.v = 0
        self.limit = limit
        self.left = x
        self.right = x + self.REC_W
        self.bottom = y
        self.top = y + self.REC_H

    def reset_bounds(self):
        self.left = self.x
        self.right = self.x + self.REC_W
        self.bottom = self.y
        self.top = self.y + self.REC_H

    def update(self, dt):
        self.y += self.v * dt
        self.y = np.clip(self.y, 0, self.limit - self.REC_H)
        self.reset_bounds()
