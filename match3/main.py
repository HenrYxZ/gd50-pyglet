import pyglet
from pyglet.text import Label
from random import random, uniform, randrange


from constants import *
from timer import Timer


window = pyglet.window.Window(WIDTH, HEIGHT, "Match 3")
label = Label(x=4*SCALE, y=HEIGHT-4*SCALE, font_size=8)
fps_label = Label(color=COLOR_FPS, font_size=MEDIUM)
fps_display = pyglet.window.FPSDisplay(window)
fps_display.label = fps_label

TIMER_MAX = 10
flappy_img = pyglet.image.load("flappy.png")
batch = pyglet.graphics.Batch()
timer = 0


def update(dt):
    global timer
    if timer < TIMER_MAX:
        timer += dt
        timer_obj.update(dt)
    label.text = f"{timer:.3f}"


@window.event
def on_draw():
    window.clear()
    batch.draw()
    label.draw()
    fps_display.draw()


if __name__ == '__main__':
    end_x = WIDTH - flappy_img.width
    # Create 1000 birds
    num_birds = 1000
    timer_obj = Timer()
    for i in range(num_birds):
        x = 0
        y = randrange(HEIGHT-24*SCALE)
        rate = uniform(1, TIMER_MAX)
        bird = pyglet.sprite.Sprite(flappy_img, x=x, y=y, batch=batch)
        timer_obj.tween(rate, bird, {"x": end_x, "opacity": 255})
    pyglet.clock.schedule_interval(update, REFRESH_RATE)
    pyglet.app.run()
