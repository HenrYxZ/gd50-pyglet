import pyglet

# Local Modules
from constants import *
from resources import textures
from state_machine import StateMachine
from states import StartState


window = pyglet.window.Window(WIDTH, HEIGHT)
main_batch = pyglet.graphics.Batch()
fps_label = pyglet.text.Label(color=COLOR_FPS, font_size=MEDIUM)
fps_display = pyglet.window.FPSDisplay(window)
fps_display.label = fps_label

background = pyglet.sprite.Sprite(textures[BACKGROUND], batch=main_batch)
background.scale_x = WIDTH / background.width
background.scale_y = HEIGHT / background.height

state_machine = StateMachine({
    START: lambda: StartState()
})
state_machine.change(START)


def update(dt):
    state_machine.update(dt)


@window.event
def on_draw():
    window.clear()
    main_batch.draw()
    state_machine.render()
    fps_display.draw()


@window.event
def on_key_press(symbol, _):
    state_machine.on_key_press(symbol)


if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, REFRESH_RATE)
    pyglet.app.run()
