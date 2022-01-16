import pyglet
from pyglet.window import key


from constants import *
from paddle import Paddle
from states import BaseState
from resources import sounds
import utils


class PlayState(BaseState):
    def __init__(self, *args):
        super().__init__(*args)
        self.pause = False
        self.paddle = Paddle()
        self.pause_label = pyglet.text.Label(
            "PAUSE", x=WIDTH/2, y=HEIGHT-(HEIGHT/2-16), font_name=FONT_NAME,
            font_size=LARGE, anchor_x='center', anchor_y='center'
        )

    def on_key_press(self, symbol):
        if symbol == key.SPACE:
            self.pause = not self.pause
            utils.play(sounds[PAUSE])

    def update(self, dt):
        if self.pause:
            return
        self.paddle.update(dt)

    def render(self):
        if self.pause:
            self.pause_label.draw()
        self.paddle.draw()
