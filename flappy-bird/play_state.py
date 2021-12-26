import random


from constants import *
from bird import Bird
from base_state import BaseState
from pipe_pair import PipePair


class PlayState(BaseState):
    def __init__(self, width, height, batch):
        super().__init__()
        self.bird = Bird(batch=batch)
        self.bird.x = width / 2
        self.bird.y = height / 2
        self.pipe_pairs = []
        self.spawn_timer = 0
        self.last_y = random.uniform(10, height * (3 / 4))
        self.width = width
        self.batch = batch
        # This is a reference to the state machine change method
        self.change_state = None
        self.batch = batch

    def spawn_pipe(self):
        x = self.width
        y = self.last_y + random.uniform(-PIPE_HEIGHT_VARY, PIPE_HEIGHT_VARY)
        pipe_pair = PipePair(x, y, batch=self.batch)
        self.pipe_pairs.append(pipe_pair)

    def update(self, dt):
        # spawn new pipes
        self.spawn_timer += dt
        if self.spawn_timer > 2:
            self.spawn_pipe()
            self.spawn_timer = 0

        # Update objects
        self.bird.update(dt)
        for pair in self.pipe_pairs:
            pair.update(dt)
            # Check collision
            if (
                self.bird.collides(pair.pipes['top']) or
                self.bird.collides(pair.pipes['bottom'])
            ):
                self.change_state(TITLE_STATE)
            # Remove pipe pairs offscreen
            if pair.x < -pair.width:
                pair.dead = True

        # only keep pipes that appear on screen
        for to_remove in [pair for pair in self.pipe_pairs if pair.dead]:
            to_remove.delete()
            self.pipe_pairs.remove(to_remove)

    def render(self):
        self.batch.draw()
