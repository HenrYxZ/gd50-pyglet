import pyglet
from pyglet.window import key

# Local imports
from constants import *
from countdown_state import CountdownState
from play_state import PlayState
from score_state import ScoreState
from score_state import keys as score_keys
from state_machine import StateMachine
from title_state import TitleScreenState
from title_state import keys as title_keys
import resources

HEIGHT = 288
WIDTH = 512

window = pyglet.window.Window(WIDTH, HEIGHT, caption="Fifty Bird")
main_batch = pyglet.graphics.Batch()
fps_label = pyglet.text.Label(color=COLOR_FPS, font_size=FLAPPY_SIZE)
fps_display = pyglet.window.FPSDisplay(window)
fps_display.label = fps_label

# Sprites
background = pyglet.sprite.Sprite(resources.bg_img, batch=main_batch)
ground = pyglet.sprite.Sprite(resources.ground_img, batch=main_batch)

# Variables
bg_scroll = 0
ground_scroll = 0

# State Machine
state_machine = StateMachine({
    PLAY_STATE: lambda: PlayState(
        WIDTH, HEIGHT, state_machine
    ),
    TITLE_STATE: lambda: TitleScreenState(
        WIDTH, HEIGHT, state_machine
    ),
    SCORE_STATE: lambda: ScoreState(
        WIDTH, HEIGHT, state_machine
    ),
    COUNTDOWN_STATE: lambda: CountdownState(
        WIDTH, HEIGHT, state_machine
    )
})
window.push_handlers(title_keys)
window.push_handlers(score_keys)
state_machine.change(TITLE_STATE)


def update(dt):
    global bg_scroll, ground_scroll
    # Parallax
    bg_scroll = (bg_scroll + BG_SCROLL_SPEED * dt) % BG_LOOP_POINT
    ground_scroll = (ground_scroll + GROUND_SCROLL_SPEED * dt) % WIDTH
    background.x = -bg_scroll
    ground.x = -ground_scroll
    state_machine.update(dt)


def init():
    pyglet.clock.schedule_interval(update, REFRESH_RATE)
    pyglet.app.run()


@window.event
def on_draw():
    window.clear()
    main_batch.draw()
    state_machine.render()
    fps_display.draw()


def on_key_press(symbol, _):
    if symbol == key.SPACE:
        if isinstance(state_machine.current, PlayState):
            state_machine.current.bird.jump()
    if symbol == key.S:
        pyglet.image.get_buffer_manager().get_color_buffer().save(
            'screenshot.png'
        )


@window.event
def on_mouse_press(_, __, button, ___):
    if button == pyglet.window.mouse.LEFT:
        if isinstance(state_machine.current, PlayState):
            state_machine.current.bird.jump()


if __name__ == '__main__':
    window.push_handlers(on_key_press=on_key_press)
    init()
