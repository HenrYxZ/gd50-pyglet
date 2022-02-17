import pyglet
from pyglet.window import key

# Local Modules
from constants import *
from paddle import keys as paddle_keys
from resources import textures, frames
from state_machine import StateMachine
from states import GameOverState, PlayState, ServeState, StartState, \
    VictoryState


window = pyglet.window.Window(WIDTH, HEIGHT)
window.push_handlers(paddle_keys)
main_batch = pyglet.graphics.Batch()
fps_label = pyglet.text.Label(color=COLOR_FPS, font_size=MEDIUM)
fps_display = pyglet.window.FPSDisplay(window)
fps_display.label = fps_label

background = pyglet.sprite.Sprite(textures[BACKGROUND], batch=main_batch)
background.scale_x = WIDTH / background.width
background.scale_y = HEIGHT / background.height

state_machine = StateMachine({
    START: lambda: StartState(state_machine),
    SERVE: lambda: ServeState(state_machine),
    PLAY: lambda: PlayState(state_machine),
    GAME_OVER: lambda: GameOverState(state_machine),
    VICTORY: lambda : VictoryState(state_machine)
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


def on_key_press(symbol, _):
    if symbol == key.S:
        pyglet.image.get_buffer_manager().get_color_buffer().save(
            'screenshot.png'
        )
    state_machine.on_key_press(symbol)


if __name__ == '__main__':
    window.push_handlers(on_key_press=on_key_press)
    pyglet.clock.schedule_interval(update, REFRESH_RATE)
    pyglet.app.run()
