import pyglet

# Local modules
from constants import PIPE_SCROLL_SPEED
import resources


class Pipe(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        super(Pipe, self).__init__(img=resources.pipe_img, *args, **kwargs)
        self.x = 0
        self.y = 0
        self.dead = False

    def update(self, dt):
        self.x -= PIPE_SCROLL_SPEED * dt
