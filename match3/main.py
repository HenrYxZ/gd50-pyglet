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
timer = 0
current_dest_idx = 0


def update(dt):
    global base_x, base_y, current_dest_idx, timer
    if current_dest_idx == len(destinations):
        return
    timer = min(MOVEMENT_TIME, timer + dt)
    if timer == MOVEMENT_TIME:
        timer = 0
        base_x = destinations[current_dest_idx]['x']
        base_y = destinations[current_dest_idx]['y']
        current_dest_idx += 1

    else:
        destination = destinations[current_dest_idx]
        bird.x = base_x + (destination['x'] - base_x) * (timer / MOVEMENT_TIME)
        bird.y = base_y + (destination['y'] - base_y) * (timer / MOVEMENT_TIME)


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
    pyglet.app.run()
