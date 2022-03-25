import pyglet
from pyglet.text import Label


from constants import *


window = pyglet.window.Window(WIDTH, HEIGHT, "Match 3")
label = Label(x=4*SCALE, y=HEIGHT-4*SCALE, font_size=8)
fps_label = Label(color=COLOR_FPS, font_size=MEDIUM)
fps_display = pyglet.window.FPSDisplay(window)
fps_display.label = fps_label

MOVE_DURATION = 2
flappy_img = pyglet.image.load("flappy.png")
timer = 0


def update(dt):
    global timer
    if timer < MOVE_DURATION:
        timer += dt
        flappy_sprite.x = min(end_x, (timer / MOVE_DURATION) * end_x)

    label.text = f"{timer:.3f}"


@window.event
def on_draw():
    window.clear()
    flappy_sprite.draw()
    label.draw()
    fps_display.draw()


if __name__ == '__main__':
    flappy_sprite = pyglet.sprite.Sprite(flappy_img, x=0, y=HEIGHT/2)
    end_x = WIDTH - flappy_sprite.width
    pyglet.clock.schedule_interval(update, REFRESH_RATE)
    pyglet.app.run()
