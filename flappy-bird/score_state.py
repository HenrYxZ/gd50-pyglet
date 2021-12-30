import pyglet
from pyglet.window import key


from base_state import BaseState
from constants import FLAPPY_FONT, FLAPPY_SIZE, MEDIUM_SIZE, PLAY_STATE


keys = key.KeyStateHandler()


class ScoreState(BaseState):
    def __init__(self, width, height, batch, state_machine):
        super().__init__()
        self.main_label = pyglet.text.Label(
            'Oof! You lost!', FLAPPY_FONT, FLAPPY_SIZE, x=width/2, y=height-64,
            anchor_x='center', anchor_y='center', batch=batch
        )
        self.score_label = pyglet.text.Label(
            '', FLAPPY_FONT, MEDIUM_SIZE, x=width/2, y=height-100, anchor_x='center',
            anchor_y='center', batch=batch
        )
        self.medium_label = pyglet.text.Label(
            'Press Enter to play again!', FLAPPY_FONT, MEDIUM_SIZE, x=width/2,
            y=height-160, anchor_x='center', anchor_y='center', batch=batch
        )
        self.batch = batch
        self.state_machine = state_machine

    def enter(self, score=0):
        self.score_label.text = f'Score: {score}'

    def render(self):
        self.batch.draw()

    def update(self, dt):
        if keys[key.ENTER]:
            self.state_machine.change(PLAY_STATE)
