import pyglet
import random

# Local imports
from bird import Bird, keys
from constants import *
from pipe import Pipe
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
pipes = []
spawn_timer = 0


def spawn_pipe():
    pipe = Pipe(batch=main_batch)
    pipe.x = WIDTH
    pipe.y = random.uniform(10, HEIGHT * (3 / 4))
    pipes.append(pipe)


def update(dt):
    global bg_scroll, ground_scroll, pipes, spawn_timer
    # Parallax
    bg_scroll = (bg_scroll + BG_SCROLL_SPEED * dt) % BG_LOOP_POINT
    ground_scroll = (ground_scroll + GROUND_SCROLL_SPEED * dt) % WIDTH
    background.x = -bg_scroll
    ground.x = -ground_scroll
    # Update objects
    bird.update(dt)
    for pipe in pipes:
        pipe.update(dt)
    # only keep pipes that appear on screen
    for to_remove in [pipe for pipe in pipes if pipe.dead]:
        to_remove.delete()
        pipes.remove(to_remove)
    # spawn new pipes
    spawn_timer += dt
    if spawn_timer > 2:
        spawn_pipe()
        spawn_timer = 0


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
