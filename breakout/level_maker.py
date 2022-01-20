import random


from brick import Brick
from constants import *


class LevelMaker:
    @staticmethod
    def create_map():
        bricks = []
        num_rows = random.randint(1, 5)
        num_cols = random.randint(7, 13)
        for j in range(num_rows):
            for i in range(num_cols):
                x = i * BRICKS_WIDTH + BRICKS_PADDING + (
                    (13 - num_cols) * LEFT_SIDE_PADDING
                )
                y = HEIGHT - ((j + 1) * BRICKS_HEIGHT)
                b = Brick(x=x, y=y)
                bricks.append(b)
        return bricks
