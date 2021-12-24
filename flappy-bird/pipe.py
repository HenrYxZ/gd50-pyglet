import pyglet

# Local modules
import resources


class Pipe(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(Pipe, self).__init__(resources.pipe_img, *args, **kwargs)
        self.top = self.y
        self.bottom = self.y - self.height
        self.left = self.x
        self.right = self.x + self.width

    def reset_bounding_box(self):
        self.left = self.x
        self.right = self.x + self.width
