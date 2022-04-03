import pyglet
from pyglet.shapes import Line


class LineRectangle:
    def __init__(
        self, x, y, width, height, border, color=(255, 255, 255), batch=None,
        group=None
    ):
        self._opacity = 255
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._border = border
        self._color = color
        self._batch = batch
        self._group = group
        if not batch:
            raise Exception("LineRectangle needs a batch")
        x2 = x + width
        y2 = y + height
        # Bottom horizontal side
        self.bottom = Line(x, y, x2, y, border, color, batch=batch, group=group)
        # Top horizontal side
        self.top = Line(x, y2, x2, y2, border, color, batch=batch, group=group)
        # Left vertical side
        self.left = Line(x, y, x, y2, border, color, batch=batch, group=group)
        # Right vertical side
        self.right = Line(
            x2, y, x2, y2, border, color, batch=batch, group=group
        )
        self.lines = [self.bottom, self.top, self.right, self.left]

    @property
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, new_value):
        self._opacity = new_value
        for line in self.lines:
            line.opacity = new_value

    @property
    def position(self):
        return self._x, self._y

    @position.setter
    def position(self, value):
        x, y = value
        x2 = x + self._width
        y2 = y + self._height
        # Bottom horizontal side
        self.bottom = Line(
            x, y, x2, y, self._border, self._color, batch=self._batch,
            group=self._group
        )
        # Top horizontal side
        self.top = Line(
            x, y2, x2, y2, self._border, self._color, batch=self._batch,
            group=self._group
        )
        # Left vertical side
        self.left = Line(
            x, y, x, y2, self._border, self._color, batch=self._batch,
            group=self._group
        )
        # Right vertical side
        self.right = Line(
            x2, y, x2, y2, self._border, self._color, batch=self._batch,
            group=self._group
        )
        self.lines = [self.bottom, self.top, self.right, self.left]
