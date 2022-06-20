import pyglet


def save_screenshot():
    pyglet.image.get_buffer_manager().get_color_buffer().save('screenshot.png')
