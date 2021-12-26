import pyglet

# Local imports
from bird import keys
from constants import *
from play_state import PlayState
from state_machine import StateMachine
from title_state import TitleScreenState
import resources

HEIGHT = 288
WIDTH = 512

window = pyglet.window.Window(WIDTH, HEIGHT, caption="Fifty Bird")
window.push_handlers(keys)
play_batch = pyglet.graphics.Batch()
title_batch = pyglet.graphics.Batch()
main_batch = pyglet.graphics.Batch()
# Sprites
background = pyglet.sprite.Sprite(resources.bg_img, batch=main_batch)
ground = pyglet.sprite.Sprite(resources.ground_img, batch=main_batch)

# Variables
bg_scroll = 0
ground_scroll = 0

# State Machine
play_state = PlayState(WIDTH, HEIGHT, play_batch)
title_state = TitleScreenState(WIDTH, HEIGHT, title_batch)
window.push_handlers(on_key_press=title_state.handle_key_event)
state_machine = StateMachine({
    PLAY_STATE: play_state, TITLE_STATE: title_state
})
play_state.change_state = state_machine.change
title_state.change_state = state_machine.change
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


if __name__ == '__main__':
    init()
