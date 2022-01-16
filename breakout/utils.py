from constants import *


def play(sound, volume=GLOBAL_VOLUME):
    player = sound.play()
    player.volume = volume
    return player


def generate_tex_regions(atlas, width, height):
    sheet_cols = atlas.width // width
    sheet_rows = atlas.height // height
    sheet_counter = 1
    sprite_sheet = {}

    for j in range(sheet_rows):
        for i in range(sheet_cols):
            x = i * width
            y = j * height
            sprite_sheet[sheet_counter] = atlas.get_region(x, y, width, height)
            sheet_counter += 1
    return sprite_sheet


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
    y = 56
    counter = 1
    texs = {}

    for i in range(4):
        texs[counter] = atlas.get_region(x, y, BALL_WIDTH, BALL_HEIGHT)
        x += 8
        counter = counter + 1

    x = 96
    y = 64

    for i in range(3):
        texs[counter] = atlas.get_region(x, y, BALL_WIDTH, BALL_HEIGHT)
        x += 8
        counter = counter + 1
    return texs
