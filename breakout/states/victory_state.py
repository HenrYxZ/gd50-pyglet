from pyglet.window import key
from pyglet.text import Label
import random


from ball import Ball
from constants import *
from level_maker import LevelMaker
from states import BaseState
from ui import render_health, render_score


class VictoryState(BaseState):
    def __init__(self, *args, **kwargs):
        super(VictoryState, self).__init__(*args, **kwargs)
        self.level = 0
        self.score = 0
        self.paddle = None
        self.health = MAX_HEALTH
        self.ball = None
        self.label = Label(x=WIDTH/2, y=3*HEIGHT/4, font_name=FONT_NAME,
            font_size=MEDIUM, anchor_x='center', anchor_y='center'
        )
        self.instructions = Label(
            "Press Enter to serve!", x=WIDTH/2, y=HEIGHT/2, font_name=FONT_NAME,
            font_size=MEDIUM, anchor_x='center', anchor_y='center'
        )

    def enter(
            self, level=0, score=0, paddle=None, health=MAX_HEALTH, ball=None
    ):
        self.level = level
        self.score = score
        self.paddle = paddle
        self.health = health
        self.ball = ball
        self.label.text = f"Level {level} complete!"

    def update(self, dt):
        self.paddle.update(dt)
        self.ball.x = (
            self.paddle.x + self.paddle.width / 2 + self.ball.width / 2
        )
        self.ball.y = self.paddle.y + self.paddle.height

    def render(self):
        self.paddle.draw()
        self.ball.draw()

        render_health(self.health)
        render_score(self.score)

        self.label.draw()
        self.instructions.draw()

    def on_key_press(self, symbol):
        if symbol == key.ENTER or symbol == key.RETURN:
            self.state_machine.change(
                SERVE,
                level=self.level+1,
                paddle=self.paddle,
                bricks=LevelMaker.create_map(self.level+1),
                health=self.health,
                score=self.score
            )
