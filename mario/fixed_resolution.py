from pyglet.gl import *
import pyglet


class FixedResolution:
    def __init__(self, window, width, height, filtered=False):
        self.window = window
        self.width = width
        self.height = height
        self._filtered = filtered
        self._viewport = 0, 0, 0, 0, 0
        self._calculate_viewport(self.window.width, self.window.height)
        self._cam_x = 0
        self._cam_y = 0
        self.clear_color = 0, 0, 0, 1

        self.texture = pyglet.image.Texture.create(width, height, rectangle=True)

        if not filtered:
            pyglet.image.Texture.default_min_filter = GL_NEAREST
            pyglet.image.Texture.default_mag_filter = GL_NEAREST
            glTexParameteri(self.texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameteri(self.texture.target, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        def on_resize(w, h):
            self._calculate_viewport(w, h)
            self.window_w, self.window_h = w, h

        self.window.on_resize = on_resize

    def _calculate_viewport(self, new_screen_width, new_screen_height):
        aspect_ratio = self.width / self.height
        aspect_width = new_screen_width
        aspect_height = aspect_width / aspect_ratio + 0.5
        if aspect_height > new_screen_height:
            aspect_height = new_screen_height
            aspect_width = aspect_height * aspect_ratio + 0.5

        if not self._filtered:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        self._viewport = (int((new_screen_width / 2) - (aspect_width / 2)),     # x
                          int((new_screen_height / 2) - (aspect_height / 2)),   # y
                          0,                                                    # z
                          int(aspect_width),                                    # width
                          int(aspect_height))                                   # height

    def __enter__(self):
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width, 0, self.height, -255, 255)
        glMatrixMode(GL_MODELVIEW)
        glTranslatef(self._cam_x, self._cam_y, 0)

    def set_camera(self, x=0, y=0):
        self._cam_x = -x
        self._cam_y = -y

    def __exit__(self, *unused):
        win = self.window
        buffer = pyglet.image.get_buffer_manager().get_color_buffer()
        self.texture.blit_into(buffer, 0, 0, 0)

        glViewport(0, 0, win.width, win.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, win.width, 0, win.height, -1, 1)
        glMatrixMode(GL_MODELVIEW)

        glClearColor(*self.clear_color)
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        self.texture.blit(*self._viewport)

    def begin(self):
        self.__enter__()

    def end(self):
        self.__exit__()
