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

    def render(self):
        for brick in filter(lambda l: l.in_play, self.bricks):
            brick.draw()

        self.paddle.draw()
        self.ball.draw()

        if self.pause:
            self.pause_label.draw()
