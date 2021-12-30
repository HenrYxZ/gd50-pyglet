import pyglet
import random


from constants import *
from bird import Bird
from base_state import BaseState
from pipe_pair import PipePair

score_str = 'Score: {0}'
batch = pyglet.graphics.Batch()


class PlayState(BaseState):
    def __init__(self, width, height, state_machine):
        super().__init__()
        self.bird = Bird(batch=batch)
        self.bird.x = width / 2
        self.bird.y = height / 2
        self.pipe_pairs = []
        self.spawn_timer = 0
        self.last_y = random.uniform(10, height * (3 / 4))
        self.width = width
        self.state_machine = state_machine
        self.score = 0
        self.score_label = pyglet.text.Label(
            score_str.format(self.score), FLAPPY_FONT, FLAPPY_SIZE, x=8,
            y=height-36
        )

    def spawn_pipe(self):
        x = self.width
        y = self.last_y + random.uniform(-PIPE_HEIGHT_VARY, PIPE_HEIGHT_VARY)
        pipe_pair = PipePair(x, y, batch=batch)
        self.pipe_pairs.append(pipe_pair)

    def update(self, dt):
        # spawn new pipes
        self.spawn_timer += dt
        if self.spawn_timer > 2:
            self.spawn_pipe()
            self.spawn_timer = 0

        # Update pipe pairs
        for pair in self.pipe_pairs:
            pair.update(dt)
            # Check collision
            if (
                self.bird.collides(pair.pipes['top']) or
                self.bird.collides(pair.pipes['bottom'])
            ):
                self.state_machine.change(SCORE_STATE, score=self.score)
            # Check score
            if not pair.scored:
                if pair.x + pair.width < self.bird.x:
                    pair.scored = True
                    self.score += 1
                    self.score_label.text = score_str.format(self.score)
            # Remove pipe pairs offscreen
            if pair.x < -pair.width:
                pair.dead = True

        # only keep pipes that appear on screen
        for to_remove in [pair for pair in self.pipe_pairs if pair.dead]:
            to_remove.delete()
            self.pipe_pairs.remove(to_remove)

        # Update bird
        self.bird.update(dt)

        # Check falling to the ground
        if self.bird.y <= GROUND_HEIGHT:
            self.state_machine.change(SCORE_STATE, score=self.score)

    def render(self):
        batch.draw()
        self.score_label.draw()
