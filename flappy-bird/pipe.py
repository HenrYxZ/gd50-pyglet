import pyglet

# Local modules
import resources


class Pipe(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(Pipe, self).__init__(resources.pipe_img, *args, **kwargs)
