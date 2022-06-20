import numpy as np
import pyglet
from pyglet.window import key
from pyglet.sprite import Sprite


from animation import Animation
from constants import *
from fixed_resolution import FixedResolution
import utils


window = pyglet.window.Window(WIDTH * 3, HEIGHT * 3, caption="tiles0")
viewport = FixedResolution(window, WIDTH, HEIGHT)
batch = pyglet.graphics.Batch()
keys = key.KeyStateHandler()
window.push_handlers(keys)

tiles_tex = pyglet.resource.image("tiles.png")
tiles = pyglet.image.ImageGrid(tiles_tex, 1, 2)

tile_map = []
map_width = 20
map_height = 9
background_color = np.random.random_sample(3)
camera_scroll = 0
GROUND_LEVEL = 3

# create tile map
for j in range(map_height):
    tile_map.append([])
    for i in range(map_width):
        tile_id = SKY_ID if j < (map_height - GROUND_LEVEL) else GROUND_ID
        tile_map[j].append(tile_id)

# create sprites
sprites = []
for j in range(map_height):
    for i in range(map_width):
        x = i * TILE_SIZE
        y = (map_height - 1 - j) * TILE_SIZE
        tile_id = tile_map[j][i]
        sprite = Sprite(tiles[tile_id - 1], x=x, y=y, batch=batch)
        sprites.append(sprite)

# Create character
character_sheet = pyglet.resource.image("character.png")
character_quads = pyglet.image.ImageGrid(character_sheet, 1, 11)
# adjust character quads to be centered in x
for img in character_quads:
    img.anchor_x = CHARACTER_WIDTH / 2

# The animations
idle_animation = Animation([0], 1)
moving_animation = Animation([9, 10], 0.2)
jump_animation = Animation([2], 1)

current_animation = idle_animation
direction = "right"

character_x = WIDTH / 2
character_y = GROUND_LEVEL * TILE_SIZE
character_sprite = Sprite(
    character_quads[0],
    x=character_x, y=character_y, batch=batch
)
character_dy = 0


def on_key_press(symbol, _):
    global character_dy, current_animation
    if symbol == key.SPACE and character_dy == 0:
        character_dy = JUMP_SPEED
        current_animation = jump_animation
    if symbol == key.S:
        utils.save_screenshot()


def update(dt):
    global camera_scroll, character_x, character_dy, character_y, \
        current_animation, direction

    # apply velocity to character y
    character_dy -= GRAVITY
    character_y += character_dy * dt

    if character_y < GROUND_LEVEL * TILE_SIZE:
        character_y = GROUND_LEVEL * TILE_SIZE
        character_dy = 0
    character_sprite.y = character_y

    current_animation.update(dt)

    if keys[key.LEFT]:
        character_sprite.x -= CHARACTER_MOVE_SPEED * dt
        direction = "left"
        if character_dy == 0:
            current_animation = moving_animation
            character_sprite.scale_x = -1
    elif keys[key.RIGHT]:
        character_sprite.x += CHARACTER_MOVE_SPEED * dt
        direction = "right"
        if character_dy == 0:
            current_animation = moving_animation
            character_sprite.scale_x = 1
    else:
        if not character_dy:
            current_animation = idle_animation
            character_sprite.scale_x = 1

    camera_scroll = character_sprite.x - WIDTH / 2 - CHARACTER_WIDTH / 2


@window.event
def on_draw():
    with viewport:
        pyglet.gl.glClearColor(*background_color, 1)
        window.clear()
        pyglet.gl.glTranslatef(int(-camera_scroll), 0, 0)
        # update character sprite
        frame_num = current_animation.get_current_frame()
        character_sprite.image = character_quads[frame_num]
        batch.draw()
        pyglet.gl.glTranslatef(int(camera_scroll), 0, 0)


if __name__ == '__main__':
    window.push_handlers(on_key_press=on_key_press)
    pyglet.clock.schedule_interval(update, 1 / FPS)
    pyglet.app.run()
