import os
import pyglet.image

from constants import *
from flip_image_grid import FlippedImageGrid


def play(sound, volume=GLOBAL_VOLUME):
    player = sound.play()
    player.volume = volume
    return player


def generate_paddle_tex(atlas):
    x = 0
    y = 176
    counter = 1
    texs = {}

    for i in range(NUM_PADDLES):
        texs[counter] = atlas.get_region(
            x, y, SMALL_PADDLE_WIDTH, PADDLE_HEIGHT
        )
        counter += 1
        texs[counter] = atlas.get_region(
            x + SMALL_PADDLE_WIDTH, y, MEDIUM_PADDLE_WIDTH, PADDLE_HEIGHT
        )
        counter += 1
        offset = SMALL_PADDLE_WIDTH + MEDIUM_PADDLE_WIDTH
        texs[counter] = atlas.get_region(
            x + offset, y, LARGE_PADDLE_WIDTH, PADDLE_HEIGHT
        )
        counter += 1
        texs[counter] = atlas.get_region(
            x, y - PADDLE_HEIGHT, MEDIUM_PADDLE_WIDTH, PADDLE_HEIGHT
        )
        counter += 1
        # Prepare y for the next set of paddles
        y -= 2 * PADDLE_HEIGHT
    return texs


def generate_ball_tex(atlas):
    x = 96
    y = atlas.height - 56
    counter = 1
    texs = {}

    for i in range(4):
        texs[counter] = atlas.get_region(x, y, BALL_WIDTH, BALL_HEIGHT)
        x += 8
        counter += 1

    x = 96
    y = atlas.height - 64

    for i in range(3):
        texs[counter] = atlas.get_region(x, y, BALL_WIDTH, BALL_HEIGHT)
        x += 8
        counter += 1
    return texs


def generate_brick_tex(atlas):
    x = 0
    bricks_cols = atlas.width // BRICKS_WIDTH
    height = BRICKS_ROWS * BRICKS_HEIGHT
    y = atlas.height - height
    bricks_region = atlas.get_region(x, y, atlas.width, height)
    bricks_seq = FlippedImageGrid(bricks_region, BRICKS_ROWS, bricks_cols)
    return bricks_seq[:22]


def read_high_scores(filename):
    scores: dict[int, dict[str, Any]] = {}
    counter = 1
    with open(filename, 'rt') as f:
        reading_name = True
        for line in f:
            if reading_name:
                scores[counter] = {"name": line[0:3]}
            else:
                scores[counter]['score'] = int(line)
                counter += 1
            reading_name = not reading_name
    return scores


def write_high_scores(high_scores):
    folder = pyglet.resource.get_settings_path('Breakout')
    filename = os.path.join(folder, 'highscores.txt')
    scores_str = ""
    for i in range(1, 11):
        scores_str += f"{high_scores[i]['name']}\n"
        scores_str += f"{high_scores[i]['score']}\n"
    with open(filename, 'wt') as f:
        f.write(scores_str)


def load_high_scores():
    folder = pyglet.resource.get_settings_path('Breakout')
    filename = os.path.join(folder, 'highscores.txt')
    if not os.path.exists(folder):
        # Make folder if it doesn't exist
        os.makedirs(folder)
        # Write a placeholder highscore
        scores_str = ""
        for i in range(10, 0, -1):
            scores_str += "CTO\n"
            scores_str += f"{i * 1000}\n"
        with open(filename, 'wt') as f:
            f.write(scores_str)
    scores = read_high_scores(filename)
    return scores
