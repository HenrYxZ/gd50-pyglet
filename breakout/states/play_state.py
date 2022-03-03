import pyglet
from pyglet.window import key
import numpy as np
import random


from ball import Ball
from breakout.constants import *
from level_maker import LevelMaker
from paddle import Paddle
from particles import ParticleSettings, ParticleSystem
from breakout.states import BaseState
from resources import sounds
import resources
from ui import render_health, render_score
import utils


def settings_by_skin_and_tier(skin, tier):
    # Use same color for start and end
    color = PALETTE_COLORS[skin]
    start_opacity = (tier + 1) * ALPHA_STEP
    end_opacity = 0
    return ParticleSettings(
        color, color, start_opacity, end_opacity, PARTICLES_MIN_LIFESPAN,
        PARTICLES_MAX_LIFESPAN
    )


PARTICLE_SETTINGS = {}

for brick_skin in range(1, NUM_BRICKS + 1):
    for brick_tier in range(NUM_BRICK_TIERS):
        PARTICLE_SETTINGS[(brick_skin, brick_tier)] = settings_by_skin_and_tier(
            brick_skin, brick_tier
        )


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
        self.level = 0
        self.particle_system = ParticleSystem(
            resources.textures[PARTICLE], MAX_PARTICLES
        )
        self.particle_system.forces.append(GRAVITY / PIXEL_SIZE)
        self.high_scores = {}
        self.recover_points = RECOVER_POINTS

    def on_key_press(self, symbol):
        if symbol == key.SPACE:
            self.pause = not self.pause
            utils.play(sounds[PAUSE])

    def enter(
        self, level=0, paddle=None, bricks=None, health=MAX_HEALTH, score=0,
        ball=None, high_scores=None
    ):
        self.level = level
        self.paddle = paddle
        self.bricks = bricks
        self.health = health
        self.score = score
        self.ball = ball
        self.high_scores = high_scores
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
            self.ball.y = self.paddle.y + self.paddle.height
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
                # Emit particles
                source_x = brick.x + brick.width / 2
                source_y = brick.y + brick.height / 2
                particle_settings = PARTICLE_SETTINGS[(brick.skin, brick.tier)]
                self.particle_system.emit(
                    source_x, source_y, PARTICLES_PER_HIT, particle_settings
                )
                # hit brick
                brick.hit()
                self.score += brick.tier * TIER_MULT + brick.skin * SKIN_MULT

                # Check for health points
                if self.score > self.recover_points:
                    self.health = min(MAX_HEALTH, self.health + 1)
                    self.recover_points *= 2
                    utils.play(resources[RECOVER])

                if self.check_victory():
                    utils.play(sounds[VICTORY])
                    self.state_machine.change(
                        VICTORY,
                        level=self.level,
                        score=self.score,
                        paddle=self.paddle,
                        health=self.health,
                        ball=self.ball,
                        high_scores=self.high_scores
                    )
                # bounce ball
                ball_right = self.ball.x + self.ball.width
                brick_top = brick.y + brick.height
                brick_right = brick.x + brick.width
                if self.ball.x + 2 < brick.x and self.ball.dx > 0:
                    # left collision
                    self.ball.dx = -self.ball.dx
                    self.ball.x = brick.x - self.ball.width
                elif ball_right + 2 > brick_right and self.ball.dx < 0:
                    # right collision
                    self.ball.dx = -self.ball.dx
                    self.ball.x = brick_right
                elif self.ball.y - 2 > brick_top:
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
                self.state_machine.change(
                    GAME_OVER, score=self.score, high_scores=self.high_scores
                )
            else:
                self.state_machine.change(
                    SERVE,
                    level=self.level,
                    paddle=self.paddle,
                    bricks=self.bricks,
                    health=self.health,
                    score=self.score,
                    high_scores=self.high_scores
                )
        # update particles
        self.particle_system.update(dt)

    def render(self):
        for brick in filter(lambda l: l.in_play, self.bricks):
            brick.draw()

        self.paddle.draw()
        self.ball.draw()

        render_health(self.health)
        render_score(self.score)

        if self.pause:
            self.pause_label.draw()
        self.particle_system.draw()

    def check_victory(self):
        for brick in self.bricks:
            if brick.in_play:
                return False
        return True
