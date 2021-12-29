import pyglet
from pyglet.window import key


from base_state import BaseState
from constants import FLAPPY_FONT, PLAY_STATE


keys = key.KeyStateHandler()


class TitleScreenState(BaseState):
    def __init__(self, width, height, batch, state_machine):
        super().__init__()
        self.name_label = pyglet.text.Label(
            'Fifty Bird', FLAPPY_FONT, 28, x=width/2, y=height-64, batch=batch
        )
        self.medium_label = pyglet.text.Label(
            'Press Enter', FLAPPY_FONT, 14, x=width/2, y=height-100, batch=batch
        )
        self.batch = batch
        self.state_machine = state_machine

    def render(self):
        self.batch.draw()

    def update(self, dt):
        if keys[key.ENTER]:
            self.state_machine.change(PLAY_STATE)
