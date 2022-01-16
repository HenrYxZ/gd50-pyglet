import numpy as np
import pyglet
from pyglet.sprite import Sprite
from pyglet.window import key


from constants import *
import resources


keys = key.KeyStateHandler()
temp_img = pyglet.image.Texture.create(10, 10)


class Paddle(Sprite):
    def __init__(self, *args, **kwargs):
        super(Paddle, self).__init__(img=temp_img, *args, **kwargs)
        self.x = WIDTH / 2 - 32
        self.y = 32
        self.dx = 0
        self.size = 2
        self.skin = 1
        paddle_number = self.size + NUM_PADDLES * (self.skin - 1)
        self.image = resources.frames[PADDLES][paddle_number]

    def update(self, dt):
        if keys[key.LEFT]:
            self.dx = -PADDLE_SPEED
        elif keys[key.RIGHT]:
            self.dx = PADDLE_SPEED
        else:
            self.dx = 0
        self.x = self.x + self.dx * dt
        self.x = np.clip(self.x, 0, WIDTH - self.width)
