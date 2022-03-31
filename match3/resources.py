import pyglet


pyglet.resource.path = ['resources']
pyglet.resource.reindex()

tiles_img = pyglet.resource.image("match3.png")
all_tiles = pyglet.image.ImageGrid(tiles_img, 9, 12)
tiles = []
for k in range(2):
    for j in range(9):
        variants = []
        for i in range(6):
            variants.append(
                all_tiles[(j, i + k * 6)]
            )
        tiles.append(variants)
