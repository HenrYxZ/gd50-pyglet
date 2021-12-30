import pyglet


from base_state import BaseState
from constants import FLAPPY_FONT, HUGE_SIZE, PLAY_STATE

# Time between counts in seconds
COUNTDOWN_TIME = 0.75


class CountdownState(BaseState):
    def __init__(self, width, height, state_machine):
        self.batch = pyglet.graphics.Batch()
        super().__init__()
        self.count = 3
        self.timer = 0
        self.main_label = pyglet.text.Label(
            f'{self.count}', FLAPPY_FONT, HUGE_SIZE, x=width/2, y=height-120,
            anchor_x='center', anchor_y='center', batch=self.batch
        )
        self.state_machine = state_machine

    def render(self):
        self.batch.draw()

    def update(self, dt):
        self.timer += dt
        if self.timer > COUNTDOWN_TIME:
            self.timer = self.timer % COUNTDOWN_TIME
            self.count -= 1
            self.main_label.text = f'{self.count}'

        if self.count == 0:
            self.state_machine.change(PLAY_STATE)
