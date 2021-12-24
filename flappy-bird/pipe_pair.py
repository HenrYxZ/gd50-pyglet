# Local modules
from constants import *
from pipe import Pipe


class PipePair:
    def __init__(self, x, y, batch=None):
        self.pipes = {}
        self.x = x
        y_top = y + GAP_HEIGHT
        pipe_top = Pipe(x, y_top, batch=batch)
        pipe_top.scale_y = -1.0
        pipe_top.bottom = pipe_top.y
        pipe_top.top = pipe_top.y + pipe_top.height
        self.width = pipe_top.width
        self.pipes['top'] = pipe_top
        self.pipes['bottom'] = Pipe(x, y, batch=batch)
        self.dead = False

    def update(self, dt):
        self.x -= PIPE_SCROLL_SPEED * dt
        self.pipes['top'].x = self.x
        self.pipes['bottom'].x = self.x
        self.pipes['top'].reset_bounding_box()
        self.pipes['bottom'].reset_bounding_box()

    def delete(self):
        self.pipes['top'].delete()
        self.pipes['bottom'].delete()
