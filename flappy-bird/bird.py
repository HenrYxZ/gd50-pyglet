import pyglet.sprite
from pyglet.window import key


# Local modules
from constants import BB_OFFSET, GRAVITY, JUMP_SPEED, JUMP
import resources
from resources import sounds
from utils import play

keys = key.KeyStateHandler()


class Bird(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        super(Bird, self).__init__(img=resources.bird_img, *args, **kwargs)
        self.dy = 0
        self.left = self.x - self.width / 2 + BB_OFFSET
        self.right = self.x + self.width / 2 - BB_OFFSET
        self.top = self.y + self.height / 2 - BB_OFFSET
        self.bottom = self.y - self.height / 2 + BB_OFFSET

    def reset_bounding_box(self):
        self.left = self.x - self.width / 2 + BB_OFFSET
        self.right = self.x + self.width / 2 - BB_OFFSET
        self.top = self.y + self.height / 2 - BB_OFFSET
        self.bottom = self.y - self.height / 2 + BB_OFFSET

    def update(self, dt):
        self.dy = self.dy + GRAVITY * dt
        self.y += self.dy
        self.reset_bounding_box()

        if keys[key.SPACE]:
            self.dy = JUMP_SPEED
            play(sounds[JUMP])

    def collides(self, pipe):
        if self.right >= pipe.left and self.left <= pipe.right:
            if self.top >= pipe.bottom and self.bottom <= pipe.top:
                return True
        return False
