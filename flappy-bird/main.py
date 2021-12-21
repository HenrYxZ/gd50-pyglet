import pyglet
from pyglet.window import key

# Local imports
from bird import Bird, keys
import resources

HEIGHT = 288
WIDTH = 512

window = pyglet.window.Window(WIDTH, HEIGHT, caption="Fifty Bird")
window.push_handlers(keys)
main_batch = pyglet.graphics.Batch()
# Sprites
background = pyglet.sprite.Sprite(resources.bg_img, batch=main_batch)
ground = pyglet.sprite.Sprite(resources.ground_img, batch=main_batch)
bird = Bird(batch=main_batch)

# Variables
bg_scroll = 0
ground_scroll = 0
BG_SCROLL_SPEED = 30
GROUND_SCROLL_SPEED = 2 * BG_SCROLL_SPEED
BG_LOOP_POINT = 413
REFRESH_RATE = 1 / 60.0


def update(dt):
    global bg_scroll, ground_scroll
    bg_scroll = (bg_scroll + BG_SCROLL_SPEED * dt) % BG_LOOP_POINT
    ground_scroll = (ground_scroll + GROUND_SCROLL_SPEED * dt) % WIDTH
    background.x = -bg_scroll
    ground.x = -ground_scroll
    bird.update(dt)


def init():
    bird.x = WIDTH / 2
    bird.y = HEIGHT / 2
    pyglet.clock.schedule_interval(update, REFRESH_RATE)
    pyglet.app.run()


@window.event
def on_draw():
    window.clear()
    main_batch.draw()


if __name__ == '__main__':
    init()
