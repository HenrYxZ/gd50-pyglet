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


def generate_board():
    board_tiles = []
    for j in range(8):
        board_tiles.append([])
        for i in range(8):
            x = i * 32
            y = j * 32
            tile = randrange(len(tiles))
            board_tiles[-1].append({
                "x": x, "y": y, "tile": tile, "grid_x": i, "grid_y": j
            })
    return board_tiles


def draw_board():
    new_sprites = []
    for row in board:
        for tile in row:
            new_sprites.append(
                pyglet.sprite.Sprite(
                    choice(tiles[tile['tile']]),
                    x=tile['x'] + offset_x,
                    y=tile['y'] + offset_y,
                    batch=batch,
                    group=background
                )
            )
    return new_sprites


def update(_):
    pass


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
    print(i, j)
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
    x = selected_tile['x'] + offset_x
    y = selected_tile['y'] + offset_y
    selected_rect.position = x, y


if __name__ == '__main__':
    board = generate_board()
    selected_tile = board[0][0]
    selected_rect = utils.LineRectangle(
        offset_x, offset_y, 32, 32, 4, color=(255, 0, 0),
        batch=batch, group=ui
    )
    selected_rect.opacity = 234
    sprites = draw_board()
    pyglet.clock.schedule(update)
    pyglet.app.run()
