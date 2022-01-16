from pyglet.sprite import Sprite


from constants import *
from resources import sounds
import resources
import utils


class Ball(Sprite):
    def __init__(self, skin, *args, **kwargs):
        super(Ball, self).__init__(
            img=resources.frames[BALLS][skin], *args, **kwargs
        )
        self.dx = 0
        self.dy = 0
        self.skin = skin

    def collides(self, target):
        if self.x > target.x + target.width or self.x + self.width < target.x:
            return False
        if self.y > target.y + target.height or self.y + self.height < target.y:
            return False
        return True

    def reset(self):
        self.x = WIDTH / 2 - 2
        self.y = HEIGHT / 2 - 2
        self.dx = 0
        self.dy = 0

    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt

        if self.x <= 0:
            self.x = 0
            self.dx = -self.dx
            utils.play(sounds[WALL_HIT])
        elif self.x >= WIDTH - self.width:
            self.x = WIDTH - self.width
            self.dx = -self.dx
            utils.play(sounds[WALL_HIT])

        if self.y >= HEIGHT - self.height:
            self.y = HEIGHT - self.height
            self.dy = -self.dy
            utils.play(sounds[WALL_HIT])
