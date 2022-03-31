import pyglet
from pyglet.text import Label
from random import choice, random, uniform, randrange


from constants import *
from timer import Timer
from resources import tiles


window = pyglet.window.Window(WIDTH, HEIGHT, "Match 3")
fps_label = Label(color=COLOR_FPS, font_size=MEDIUM)
fps_display = pyglet.window.FPSDisplay(window)
fps_display.label = fps_label

batch = pyglet.graphics.Batch()


def generate_board():
    board_tiles = []
    for j in range(8):
        board_tiles.append([])
        for i in range(8):
            x = i * 32
            y = j * 32
            tile = randrange(len(tiles))
            board_tiles[-1].append({"x": x, "y": y, "tile": tile})
    return board_tiles


def draw_board(offset_x, offset_y):
    new_sprites = []
    for row in board:
        for tile in row:
            new_sprites.append(
                pyglet.sprite.Sprite(
                    choice(tiles[tile['tile']]),
                    x=tile['x'] + offset_x,
                    y=tile['y'] + offset_y,
                    batch=batch
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


if __name__ == '__main__':
    board = generate_board()
    sprites = draw_board(128, 16)
    pyglet.clock.schedule(update)
    pyglet.app.run()
