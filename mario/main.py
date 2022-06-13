import numpy as np
import pyglet
from pyglet.sprite import Sprite


from constants import *


window = pyglet.window.Window(WIDTH, HEIGHT, caption="tiles0")
batch = pyglet.graphics.Batch()

tiles_tex = pyglet.resource.image("tiles.png")
tiles = pyglet.image.ImageGrid(tiles_tex, 1, 2)

tile_map = []
map_width = 16
map_height = 9
background_color = np.random.random_sample(3)
pyglet.gl.glClearColor(*background_color, 1)

# create tile map
for j in range(map_height):
    tile_map.append([])
    for i in range(map_width):
        tile_id = SKY_ID if j < 5 else GROUND_ID
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


@window.event
def on_draw():
    window.clear()
    batch.draw()


if __name__ == '__main__':
    pyglet.app.run()
