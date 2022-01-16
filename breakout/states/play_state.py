import pyglet
from pyglet.window import key
import random


from ball import Ball
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
        self.ball = Ball(random.randint(1, NUM_BALLS))
        self.pause_label = pyglet.text.Label(
            "PAUSE", x=WIDTH/2, y=HEIGHT-(HEIGHT/2-16), font_name=FONT_NAME,
            font_size=LARGE, anchor_x='center', anchor_y='center'
        )

        self.ball.dx = random.randint(-200, 200)
        self.ball.dy = random.randint(50, 60)
        self.ball.x = WIDTH / 2 - 4
        self.ball.y = 42

    def on_key_press(self, symbol):
        if symbol == key.SPACE:
            self.pause = not self.pause
            utils.play(sounds[PAUSE])

    def update(self, dt):
        if self.pause:
            return
        self.paddle.update(dt)
        self.ball.update(dt)
        # Handle collision with paddle
        if self.ball.collides(self.paddle):
            self.ball.dy = -self.ball.dy
            self.ball.y = self.paddle.y + self.paddle.height + 1
            utils.play(sounds[PADDLE_HIT])

    def render(self):
        self.paddle.draw()
        self.ball.draw()

        if self.pause:
            self.pause_label.draw()
