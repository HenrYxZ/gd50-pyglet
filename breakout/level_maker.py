import math
import random


from brick import Brick
from constants import *


class LevelMaker:
    @staticmethod
    def create_map(level):
        bricks = []
        num_rows = random.randint(1, 5)
        num_cols = random.randint(7, 13)
        if num_cols % 2 == 0:
            num_cols += 1

        highest_tier = min(3, level // 5)
        highest_skin = min(5, level % 5 + 3)

        for j in range(num_rows):
            # Random placement for each row
            skip_pattern = random.random() < 0.5
            alternate_pattern = random.random() < 0.5

            skin_1 = random.randint(1, highest_skin)
            skin_2 = random.randint(1, highest_skin)
            tier_1 = random.randint(0, highest_tier)
            tier_2 = random.randint(0, highest_tier)

            skip_flag = random.random() < 0.5
            alternate_flag = random.random() < 0.5

            for i in range(num_cols):
                if skip_pattern:
                    if skip_flag:
                        continue
                    else:
                        skip_flag = not skip_flag
                x = i * BRICKS_WIDTH + BRICKS_PADDING + (
                    (13 - num_cols) * LEFT_SIDE_PADDING
                )
                y = HEIGHT - ((j + 1) * BRICKS_HEIGHT)
                b = Brick(x=x, y=y)
                if alternate_pattern:
                    if alternate_flag:
                        b.skin = skin_1
                        b.tier = tier_1
                    else:
                        b.skin = skin_2
                        b.tier = tier_2
                    alternate_flag = not alternate_flag
                else:
                    b.skin = skin_1
                    b.tier = tier_1
                b.set_image_from_skin()
                bricks.append(b)
        if not bricks:
            bricks = LevelMaker.create_map(level)
        return bricks
