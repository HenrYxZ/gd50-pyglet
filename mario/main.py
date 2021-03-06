import numpy as np
import pyglet
from pyglet.sprite import Sprite
from pyglet.window import key
import random


from animation import Animation
from constants import *
from fixed_resolution import FixedResolution
from utils import FlippedImageGrid as ImageGrid
import utils


window = pyglet.window.Window(WIDTH * 3, HEIGHT * 3, caption="tiles0")
viewport = FixedResolution(window, WIDTH, HEIGHT)
batch = pyglet.graphics.Batch()
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)
keys = key.KeyStateHandler()
window.push_handlers(keys)

# Tiles
tiles_tex = pyglet.resource.image("tiles.png")
tile_regions = ImageGrid(tiles_tex, TILE_SET_ROWS, TILE_SET_COLS)
tile_sets = []
for region in tile_regions:
    tile_sets.append(ImageGrid(region, TILE_ROWS, TILE_COLS))

toppers_tex = pyglet.resource.image("tile_tops.png")
topper_regions = ImageGrid(toppers_tex, TOPPERS_ROWS, TOPPERS_COLS)
topper_sets = []
for region in topper_regions:
    topper_sets.append(ImageGrid(region, TILE_ROWS, TILE_COLS))

tile_set = random.choice(tile_sets)
topper_set = random.choice(topper_sets)

tile_map = []
map_width = 20
map_height = 9
background_color = np.random.random_sample(3)
camera_scroll = 0
GROUND_LEVEL = 3
level_sprites = []

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


def generate_level():
    tiles = [
        [
            {"tile_id": SKY_ID, "topper": False} for _ in range(map_width)
        ] for __ in range(map_height)
    ]

    for i in range(map_width):
        spawn_pillar = random.randint(1, 5) == 1
        if spawn_pillar:
            for j in range(GROUND_LEVEL, 7):
                tiles[map_height - 1 - j][i] = {
                    "tile_id": GROUND_ID, "topper": j == 6
                }
        for j in range(GROUND_LEVEL):
            tiles[map_height - 1 - j][i] = {
                "tile_id": GROUND_ID,
                "topper": not spawn_pillar and j == GROUND_LEVEL - 1
            }

    return tiles


def create_level_sprites():
    """
    Create the sprites for the level using the tiles map
    """
    global level_sprites
    level_sprites = []
    for j in range(len(tile_map)):
        for i in range(len(tile_map[0])):
            tile_id = tile_map[j][i]['tile_id']
            topper = tile_map[j][i]['topper']
            x = TILE_SIZE * i
            y = TILE_SIZE * (map_height - 1 - j)
            sprite = Sprite(
                tile_set[tile_id], x=x, y=y, batch=batch, group=background
            )
            level_sprites.append(sprite)
            if topper:
                sprite = Sprite(
                    topper_set[tile_id], x=x, y=y, batch=batch, group=foreground
                )
                level_sprites.append(sprite)


def on_key_press(symbol, _):
    global character_dy, current_animation, tile_map, tile_set, topper_set
    if symbol == key.SPACE and character_dy == 0:
        character_dy = JUMP_SPEED
        current_animation = jump_animation
    if symbol == key.R:
        tile_set = random.choice(tile_sets)
        topper_set = random.choice(topper_sets)
        tile_map = generate_level()
        create_level_sprites()
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
    tile_map = generate_level()
    create_level_sprites()
    window.push_handlers(on_key_press=on_key_press)
    pyglet.clock.schedule_interval(update, 1 / FPS)
    pyglet.app.run()
