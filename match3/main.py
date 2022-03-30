import pyglet
from pyglet.text import Label
from random import random, uniform, randrange


from constants import *
from timer import Timer


window = pyglet.window.Window(WIDTH, HEIGHT, "Match 3")
fps_label = Label(color=COLOR_FPS, font_size=MEDIUM)
fps_display = pyglet.window.FPSDisplay(window)
fps_display.label = fps_label

MOVEMENT_TIME = 2
flappy_img = pyglet.image.load("flappy.png")
batch = pyglet.graphics.Batch()


def update(dt):
    timer.update(dt)


@window.event
def on_draw():
    window.clear()
    batch.draw()
    fps_display.draw()


if __name__ == '__main__':
    end_x = WIDTH - flappy_img.width
    end_y = HEIGHT - flappy_img.height
    # Create 1000 birds
    destinations = [
        {"x": end_x, "y": end_y},
        {"x": end_x, "y": 0},
        {"x": 0, "y": 0},
        {"x": 0, "y": end_y},
    ]
    base_x = 0
    base_y = end_y
    bird = pyglet.sprite.Sprite(flappy_img, x=base_x, y=base_y, batch=batch)
    pyglet.clock.schedule_interval(update, REFRESH_RATE)
    timer = Timer()
    timer.tween(MOVEMENT_TIME, bird, destinations[0]).finish(
        lambda: timer.tween(MOVEMENT_TIME, bird, destinations[1]).finish(
            lambda: timer.tween(MOVEMENT_TIME, bird, destinations[2]).finish(
                lambda: timer.tween(MOVEMENT_TIME, bird, destinations[3])
            )
        )
    )
    pyglet.app.run()
