import pyglet
from pyglet.sprite import Sprite


from constants import *
from resources import sounds
import resources
import utils


temp_img = pyglet.image.Texture.create(10, 10)


class Brick(Sprite):
    def __init__(self, *args, **kwargs):
        super(Brick, self).__init__(img=temp_img, *args, **kwargs)
        self.tier = 0
        self.skin = 1
        self.in_play = True

    def hit(self):
        utils.play(sounds[BRICK_HIT_2])
        # manage tiers and colors
        if self.tier > 0:
            if self.skin == 1:
                self.tier -= 1
                self.skin = 5
            else:
                self.skin -= 1
        else:
            if self.skin == 1:
                self.in_play = False
                utils.play(sounds[BRICK_HIT_1])
            else:
                self.skin -= 1

        self.set_image_from_skin()

    def set_image_from_skin(self):
        image_idx = (self.skin - 1) * 4 + self.tier  # idx starting from 0
        self.image = resources.frames[BRICKS][image_idx]
