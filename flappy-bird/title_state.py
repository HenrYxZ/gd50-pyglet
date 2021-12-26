import pyglet
from pyglet.window import key


from base_state import BaseState
from constants import FLAPPY_FONT, PLAY_STATE


class TitleScreenState(BaseState):
    def __init__(self, width, height, batch):
        super().__init__()
        self.change_state = None
        self.name_label = pyglet.text.Label(
            'Fifty Bird', FLAPPY_FONT, 28, x=width/2, y=height-64, batch=batch
        )
        self.medium_label = pyglet.text.Label(
            'Press Enter', FLAPPY_FONT, 14, x=width/2, y=height-100, batch=batch
        )
        self.batch = batch

    def handle_key_event(self, symbol, _):
        if symbol == key.ENTER:
            self.change_state(PLAY_STATE)

    def render(self):
        self.batch.draw()
