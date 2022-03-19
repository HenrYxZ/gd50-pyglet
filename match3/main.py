import pyglet


from constants import *


timer = 0
current_second = 0


window = pyglet.window.Window(WIDTH, HEIGHT, "Match 3")
label = pyglet.text.Label(
    x=WIDTH/2, y=HEIGHT/2+SCALE*6, anchor_x='center', anchor_y='center'
)
fps_label = pyglet.text.Label(color=COLOR_FPS)
fps_display = pyglet.window.FPSDisplay(window)

def update(dt):
    global timer, current_second
    timer += dt
    if timer > 1:
        current_second += 1
        timer = timer % 1
    label.text = f"Timer: {current_second} seconds"


@window.event
def on_draw():
    window.clear()
    label.draw()
    fps_display.draw()


if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, REFRESH_RATE)
    pyglet.app.run()
