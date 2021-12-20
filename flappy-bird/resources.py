import pyglet


def center_image(image):
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


pyglet.resource.path = ['./resources']
pyglet.resource.reindex()

bg_img = pyglet.resource.image("background.png")
ground_img = pyglet.resource.image("ground.png")
bird_img = pyglet.resource.image("bird.png")

center_image(bird_img)