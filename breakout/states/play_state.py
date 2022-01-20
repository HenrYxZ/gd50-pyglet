import pyglet
from pyglet.window import key
import random


from ball import Ball
from constants import *
from level_maker import LevelMaker
from paddle import Paddle
from states import BaseState
from resources import sounds
import resources
import utils


class PlayState(BaseState):
    def __init__(self, *args):
        super().__init__(*args)
        self.pause = False
        self.paddle = Paddle()
        self.ball = Ball(random.randint(1, NUM_BALLS), x=WIDTH/2-4, y=42)
        self.pause_label = pyglet.text.Label(
            "PAUSE", x=WIDTH/2, y=HEIGHT-(HEIGHT/2-16), font_name=FONT_NAME,
            font_size=LARGE, anchor_x='center', anchor_y='center'
        )
        self.bricks = LevelMaker.create_map()
        self.ball.dx = random.randint(-200, 200)
        self.ball.dy = random.randint(50, 60)

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
        # Handle collision with bricks that are in play
        for brick in filter(lambda l: l.in_play, self.bricks):
            if self.ball.collides(brick):
                brick.hit()

    def render(self):
        for brick in filter(lambda l: l.in_play, self.bricks):
            brick.draw()

        self.paddle.draw()
        self.ball.draw()

        if self.pause:
            self.pause_label.draw()
