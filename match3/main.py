import pyglet


from constants import *
from timer import SingleTimer, Timer


window = pyglet.window.Window(WIDTH, HEIGHT, "Match 3")
labels = []
fps_label = pyglet.text.Label(color=COLOR_FPS, font_size=MEDIUM)
fps_display = pyglet.window.FPSDisplay(window)
fps_display.label = fps_label


def update(dt):
    timer.update(dt)
    for i, label in enumerate(labels):
        label.text = f"Timer: {timer.items[i].counter} seconds"


@window.event
def on_draw():
    window.clear()
    for label in labels:
        label.draw()
    fps_display.draw()


if __name__ == '__main__':
    intervals = [1, 2, 4, 3, 2]
    n = len(intervals)
    timer = Timer()
    for interval in intervals:
        timer.schedule(interval)
    for j in range(n):
        labels.append(
            pyglet.text.Label(
                x=WIDTH/2, y=HEIGHT-(70+j*16)*SCALE,
                anchor_x='center',
                anchor_y='center'
            )
        )
    pyglet.clock.schedule_interval(update, REFRESH_RATE)
    pyglet.app.run()
