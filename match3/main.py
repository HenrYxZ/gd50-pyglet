import pyglet
from pyglet.window import key
from pyglet.text import Label
from random import choice, random, uniform, randrange


from constants import *
from timer import Timer
from resources import tiles
import utils


window = pyglet.window.Window(WIDTH, HEIGHT, "Match 3")
fps_label = Label(color=COLOR_FPS, font_size=MEDIUM)
fps_display = pyglet.window.FPSDisplay(window)
fps_display.label = fps_label

batch = pyglet.graphics.Batch()

background = pyglet.graphics.OrderedGroup(0)
ui = pyglet.graphics.OrderedGroup(1)

highlighted_tile = False
highlighted_x = 0
highlighted_y = 0

offset_x = 128
offset_y = 16

timer = Timer()


def generate_board():
    board_tiles = []
    for j in range(8):
        board_tiles.append([])
        for i in range(8):
            x = i * 32
            y = j * 32
            tile = randrange(len(tiles))
            tile_sprite = pyglet.sprite.Sprite(
                choice(tiles[tile]),
                x=x + offset_x,
                y=y + offset_y,
                batch=batch,
                group=background
            )
            board_tiles[-1].append({
                "x": x, "y": y, "tile": tile_sprite, "grid_x": i, "grid_y": j
            })
    return board_tiles


def update(dt):
    timer.update(dt)


@window.event
def on_draw():
    window.clear()
    batch.draw()
    fps_display.draw()


@window.event
def on_key_press(symbol, _):
    global highlighted_x, highlighted_y, highlighted_tile, selected_rect, \
        selected_tile
    i, j = selected_tile['grid_x'], selected_tile['grid_y']
    if symbol == key.UP:
        if j < 7:
            selected_tile = board[j + 1][i]
    elif symbol == key.DOWN:
        if j > 0:
            selected_tile = board[j - 1][i]
    elif symbol == key.LEFT:
        if i > 0:
            selected_tile = board[j][i - 1]
    elif symbol == key.RIGHT:
        if i < 7:
            selected_tile = board[j][i + 1]
    if symbol == key.ENTER or symbol == key.RETURN:
        if not highlighted_tile:
            highlighted_tile = True
            highlighted_x = selected_tile['grid_x']
            highlighted_y = selected_tile['grid_y']
            x = selected_tile['x'] + offset_x
            y = selected_tile['y'] + offset_y
            highlighted_rect.position = x, y
            highlighted_rect.visible = True
        else:
            # Swap tiles
            tile1 = selected_tile
            tile2 = board[highlighted_y][highlighted_x]
            temp_x, temp_y = tile2['x'], tile2['y']
            temp_grid_x, temp_grid_y = tile2['grid_x'], tile2['grid_y']
            # Change sprites
            sprite1 = tile1['tile']
            sprite2 = tile2['tile']
            timer.tween(
                0.2,
                {
                    sprite2: {
                        'x': tile1['x'] + offset_x,
                        'y': tile1['y'] + offset_y
                    },
                    sprite1: {
                        'x': temp_x + offset_x, 'y': temp_y + offset_y
                    }
                }
            )

            temp_tile = tile1
            board[tile1['grid_y']][tile1['grid_x']] = tile2
            board[tile2['grid_y']][tile2['grid_x']] = temp_tile

            tile2['x'], tile2['y'] = tile1['x'], tile1['y']
            tile2['grid_x'], tile2['grid_y'] = tile1['grid_x'], tile1['grid_y']
            tile1['x'], tile1['y'] = temp_x, temp_y
            tile1['grid_x'], tile1['grid_y'] = temp_grid_x, temp_grid_y

            highlighted_tile = False
            highlighted_rect.visible = False
            selected_tile = tile2

    # Update selected rectangle
    x = selected_tile['x'] + offset_x
    y = selected_tile['y'] + offset_y
    selected_rect.position = x, y


if __name__ == '__main__':
    board = generate_board()
    selected_tile = board[7][0]
    selected_rect = utils.LineRectangle(
        selected_tile['x'] + offset_x,
        selected_tile['y'] + offset_y,
        32, 32, 4, color=(255, 0, 0), batch=batch, group=ui
    )
    selected_rect.opacity = 234
    highlighted_rect = pyglet.shapes.Rectangle(
        0, 0, 32, 32, batch=batch, group=ui
    )
    highlighted_rect.opacity = 128
    highlighted_rect.visible = False
    pyglet.clock.schedule(update)
    pyglet.app.run()
