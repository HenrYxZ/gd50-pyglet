import pyglet

# Local modules
from constants import *
import utils


pyglet.resource.path = ['fonts', 'graphics', 'sounds']
pyglet.resource.reindex()

# Textures
textures = {
    BACKGROUND: pyglet.resource.image("background.png"),
    MAIN: pyglet.resource.image("breakout.png"),
    ARROWS: pyglet.resource.image("arrows.png"),
    HEARTS: pyglet.resource.image("hearts.png"),
    PARTICLE: pyglet.resource.image("particle.png")
}

# Fonts
pyglet.resource.add_font("font.ttf")
pyglet.font.load(FONT_NAME)

# Sounds
sounds = {
    PADDLE_HIT: pyglet.resource.media("paddle_hit.wav", streaming=False),
    SCORE: pyglet.resource.media("score.wav", streaming=False),
    WALL_HIT: pyglet.resource.media("wall_hit.wav", streaming=False),
    CONFIRM: pyglet.resource.media("confirm.wav", streaming=False),
    SELECT: pyglet.resource.media("select.wav", streaming=False),
    NO_SELECT: pyglet.resource.media("no-select.wav", streaming=False),
    BRICK_HIT_1: pyglet.resource.media("brick-hit-1.wav", streaming=False),
    BRICK_HIT_2: pyglet.resource.media("brick-hit-2.wav", streaming=False),
    HURT: pyglet.resource.media("hurt.wav", streaming=False),
    VICTORY: pyglet.resource.media("victory.wav", streaming=False),
    RECOVER: pyglet.resource.media("recover.wav", streaming=False),
    HIGH_SCORE: pyglet.resource.media("high_score.wav", streaming=False),
    PAUSE: pyglet.resource.media("pause.wav", streaming=False),
    MUSIC: pyglet.resource.media("music.wav")
}

# Frames (texture regions)
frames = {
    PADDLES: utils.generate_paddle_tex(textures[MAIN]),
    BALLS: utils.generate_ball_tex(textures[MAIN]),
    BRICKS: utils.generate_brick_tex(textures[MAIN]),
    HEARTS: pyglet.image.ImageGrid(textures[HEARTS], 1, 2),
    ARROWS: pyglet.image.ImageGrid(textures[ARROWS], 1, 2)
}
