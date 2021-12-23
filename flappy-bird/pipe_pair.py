# Local modules
from constants import *
from pipe import Pipe


class PipePair:
    def __init__(self, x, y, batch=None):
        self.x = x
        self.pipes = {}
        y_top = y + GAP_HEIGHT
        pipe_top = Pipe(x, y_top, batch=batch)
        pipe_top.scale_y = -1
        self.pipes['top'] = pipe_top
        self.pipes['bottom'] = Pipe(x, y, batch=batch)
        self.dead = False

    def update(self, dt):
        for pipe in self.pipes.values():
            pipe.x -= PIPE_SCROLL_SPEED * dt

    def delete(self):
        self.pipes['top'].delete()
        self.pipes['bottom'].delete()
