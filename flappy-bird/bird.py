import pyglet.sprite
from pyglet.window import key


# Local modules
from constants import GRAVITY, JUMP_SPEED
import resources

keys = key.KeyStateHandler()


class Bird(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        super(Bird, self).__init__(img=resources.bird_img, *args, **kwargs)
        self.dy = 0

    def update(self, dt):
        self.dy = self.dy + GRAVITY * dt
        self.y += self.dy

        if keys[key.SPACE]:
            self.dy = JUMP_SPEED
