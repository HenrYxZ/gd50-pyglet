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
from ui import render_health, render_score
import utils


class PlayState(BaseState):
    def __init__(self, *args):
        super().__init__(*args)
        self.pause = False
        self.paddle = None
        self.ball = None
        self.bricks = None
        self.pause_label = pyglet.text.Label(
            "PAUSE", x=WIDTH/2, y=HEIGHT-(HEIGHT/2-16), font_name=FONT_NAME,
            font_size=LARGE, anchor_x='center', anchor_y='center'
        )
        self.health = MAX_HEALTH
        self.score = 0

    def on_key_press(self, symbol):
        if symbol == key.SPACE:
            self.pause = not self.pause
            utils.play(sounds[PAUSE])

    def enter(
        self, paddle=None, bricks=None, health=MAX_HEALTH, score=0, ball=None
    ):
        self.paddle = paddle
        self.bricks = bricks
        self.health = health
        self.score = score
        self.ball = ball
        self.ball.dx = random.randrange(-200, 200)
        self.ball.dy = random.randrange(50, 60)

    def update(self, dt):
        if self.pause:
            return
        self.paddle.update(dt)
        self.ball.update(dt)
        # Handle collision with paddle
        if self.ball.collides(self.paddle):
            self.ball.dy = -self.ball.dy
            self.ball.y = self.paddle.y + self.paddle.height + 1
            # Add angle influence
            paddle_center = self.paddle.x + self.paddle.width / 2
            ball_center = self.ball.x + self.ball.width / 2
            dist_paddle_ball_x = paddle_center - ball_center
            if ball_center < paddle_center and self.paddle.dx < 0:
                # ball coming from the left
                self.ball.dx = (
                    -BALL_BOUNCE_SPEED -
                    BALL_BOUNCE_FACTOR * dist_paddle_ball_x
                )
            elif ball_center > paddle_center and self.paddle.dx > 0:
                # ball coming from right
                self.ball.dx = (
                    BALL_BOUNCE_SPEED +
                    BALL_BOUNCE_FACTOR * abs(dist_paddle_ball_x)
                )

            utils.play(sounds[PADDLE_HIT])
        # Handle collision with bricks that are in play
        for brick in filter(lambda l: l.in_play, self.bricks):
            if self.ball.collides(brick):
                brick.hit()
                self.score += SCORE_PER_BLOCK
                # bounce ball
                ball_right = self.ball.x + self.ball.width
                ball_top = self.ball.y + self.ball.height
                brick_top = brick.y + brick.height
                brick_right = brick.x + brick.width
                if ball_right - 2 < brick.x and self.ball.dx > 0:
                    # left collision
                    self.ball.dx = -self.ball.dx
                    self.ball.x = brick.x - self.ball.width
                elif ball_right + 2 > brick_right and self.ball.dx < 0:
                    # right collision
                    self.ball.dx = -self.ball.dx
                    self.ball.x = brick_right
                elif ball_top < brick_top:
                    # top collision
                    self.ball.dy = -self.ball.dy
                    self.ball.y = brick_top
                else:
                    # bottom collision
                    self.ball.dy = -self.ball.dy
                    self.ball.y = brick.y - self.ball.height
                # Apply small factor for momentum
                self.ball.dy *= BALL_DY_FACTOR
                # Only allow collision with one brick
                break
        # Handle losing a point
        if self.ball.y < 0:
            self.health -= 1
            utils.play(sounds[HURT])

            if self.health == 0:
                self.state_machine.change(GAME_OVER, score=self.score)
            else:
                self.state_machine.change(
                    SERVE,
                    paddle=self.paddle,
                    bricks=self.bricks,
                    health=self.health,
                    score=self.score
                )

    def render(self):
        for brick in filter(lambda l: l.in_play, self.bricks):
            brick.draw()

        self.paddle.draw()
        self.ball.draw()

        render_health(self.health)
        render_score(self.score)

        if self.pause:
            self.pause_label.draw()
