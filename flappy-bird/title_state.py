import pyglet
from pyglet.window import key


from base_state import BaseState
from constants import *


keys = key.KeyStateHandler()
batch = pyglet.graphics.Batch()


class TitleScreenState(BaseState):
    def __init__(self, width, height, state_machine):
        super().__init__()
        self.name_label = pyglet.text.Label(
            'Fifty Bird', FLAPPY_FONT, FLAPPY_SIZE, x=width/2, y=height-64,
            batch=batch
        )
        self.medium_label = pyglet.text.Label(
            'Press Enter', FLAPPY_FONT, MEDIUM_SIZE, x=width/2, y=height-100,
            batch=batch
        )
        self.state_machine = state_machine

    def render(self):
        batch.draw()

    def update(self, dt):
        if keys[key.ENTER]:
            self.state_machine.change(COUNTDOWN_STATE)
