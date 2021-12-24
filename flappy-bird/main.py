import pyglet
import random

# Local imports
from bird import Bird, keys
from constants import *
from pipe_pair import PipePair
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
pipe_pairs = []
spawn_timer = 0
last_y = random.uniform(10, HEIGHT * (3 / 4))
scrolling = True


def spawn_pipe():
    x = WIDTH
    y = last_y + random.uniform(-PIPE_HEIGHT_VARY, PIPE_HEIGHT_VARY)
    pipe_pair = PipePair(x, y, batch=main_batch)
    pipe_pairs.append(pipe_pair)


def update(dt):
    global bg_scroll, ground_scroll, pipe_pairs, scrolling, spawn_timer
    if not scrolling:
        return
    # Parallax
    bg_scroll = (bg_scroll + BG_SCROLL_SPEED * dt) % BG_LOOP_POINT
    ground_scroll = (ground_scroll + GROUND_SCROLL_SPEED * dt) % WIDTH
    background.x = -bg_scroll
    ground.x = -ground_scroll
    # Update objects
    bird.update(dt)
    for pipe_pair in pipe_pairs:
        pipe_pair.update(dt)
        # Check collision
        if (
            bird.collides(pipe_pair.pipes['top']) or
            bird.collides(pipe_pair.pipes['bottom'])
        ):
            scrolling = False
        # Remove pipe pairs offscreen
        if pipe_pair.x < -pipe_pair.width:
            pipe_pair.dead = True
    # only keep pipes that appear on screen
    for to_remove in [pipe_pair for pipe_pair in pipe_pairs if pipe_pair.dead]:
        to_remove.delete()
        pipe_pairs.remove(to_remove)
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
