import pyglet.sprite


# Local modules
import resources


class Bird(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(Bird, self).__init__(img=resources.bird_img, *args, **kwargs)

