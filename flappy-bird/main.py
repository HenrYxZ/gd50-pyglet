import pyglet


# Local imports
import resources

HEIGHT = 288
WIDTH = 512

window = pyglet.window.Window(WIDTH, HEIGHT)
main_batch = pyglet.graphics.Batch()
# Sprites
background = pyglet.sprite.Sprite(resources.bg_img, batch=main_batch)
ground = pyglet.sprite.Sprite(resources.ground_img, batch=main_batch)


def init():
    pyglet.app.run()


@window.event
def on_draw():
    window.clear()
    main_batch.draw()


if __name__ == '__main__':
    init()
