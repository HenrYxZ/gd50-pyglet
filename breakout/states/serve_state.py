from pyglet.window import key
from pyglet.text import Label
import random


from ball import Ball
from constants import *
from breakout.states import BaseState
from ui import render_health, render_score


class ServeState(BaseState):
    def __init__(self, *args, **kwargs):
        super(ServeState, self).__init__(*args, **kwargs)
        self.level = 0
        self.paddle = None
        self.ball = None
        self.bricks = None
        self.health = MAX_HEALTH
        self.score = 0
        self.high_scores = {}
        self.lvl_label = Label(
            x=WIDTH/2, y=3*HEIGHT/4, font_name=FONT_NAME, font_size=LARGE,
            anchor_x='center', anchor_y='center'
        )
        self.label = Label(
            "Press Enter to serve!", x=WIDTH/2, y=HEIGHT/2, font_name=FONT_NAME,
            font_size=MEDIUM, anchor_x='center', anchor_y='center'
        )

    def enter(
        self, level=0, paddle=None, bricks=None, health=MAX_HEALTH, score=0,
        high_scores=None
    ):
        self.level = level
        self.paddle = paddle
        self.bricks = bricks
        self.health = health
        self.score = score
        self.high_scores = high_scores
        self.lvl_label.text = f"Level {level}"

        ball_skin = random.randint(1, NUM_BALLS)
        self.ball = Ball(ball_skin)

    def update(self, dt):
        self.paddle.update(dt)
        self.ball.x = (
            self.paddle.x + self.paddle.width / 2 + self.ball.width / 2
        )
        self.ball.y = self.paddle.y + self.paddle.height

    def render(self):
        self.paddle.draw()
        self.ball.draw()

        for brick in filter(lambda l: l.in_play, self.bricks):
            brick.draw()

        render_health(self.health)
        render_score(self.score)

        self.lvl_label.draw()
        self.label.draw()

    def on_key_press(self, symbol):
        if symbol == key.ENTER or symbol == key.RETURN:
            self.state_machine.change(
                PLAY,
                level=self.level,
                paddle=self.paddle,
                bricks=self.bricks,
                health=self.health,
                score=self.score,
                ball=self.ball,
                high_scores=self.high_scores
            )
