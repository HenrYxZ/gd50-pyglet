import pyglet.sprite


# Local modules
from constants import GRAVITY
import resources


class Bird(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(Bird, self).__init__(img=resources.bird_img, *args, **kwargs)

        self.dy = 0

    def update(self, dt):
        self.dy = self.dy + GRAVITY * dt
        self.y -= self.dy
