import numpy as np


# Screen
WIDTH = 432
HEIGHT = 243
COLOR_FPS = (0, 255, 0, 75)
REFRESH_RATE = 1 / 120

# Fonts
SMALL = 8
MEDIUM = 16
LARGE = 32
FONT_NAME = '04b03'
COLOR_HIGHLIGHTED = (103, 255, 255, 255)
WHITE = (255, 255, 255, 255)

# Textures
BACKGROUND = 'background'
MAIN = 'main'
ARROWS = 'arrows'
HEARTS = 'hearts'
PARTICLE = 'particle'
MAIN_FLIP_Y = 'main_flip_y'

NUM_PADDLES = 4
SMALL_PADDLE_WIDTH = 32
MEDIUM_PADDLE_WIDTH = 64
LARGE_PADDLE_WIDTH = 96
XL_PADDLE_WIDTH = 128
PADDLE_HEIGHT = 16

BALL_WIDTH = 8
BALL_HEIGHT = 8
NUM_BALLS = 7

BRICKS_WIDTH = 32
BRICKS_HEIGHT = 16
BRICKS_ROWS = 4
NUM_BRICKS = 5
NUM_BRICK_TIERS = 4

PALETTE_COLORS = {
    # blue
    1: np.array([99, 155, 255]),
    # green
    2: np.array([106, 190, 47]),
    # red
    3: np.array([217, 87, 99]),
    # purple
    4: np.array([215, 123, 186]),
    # gold
    5: np.array([251, 242, 54])
}
MAX_PARTICLES = 256
PARTICLES_PER_HIT = 64
ALPHA_STEP = 55
PARTICLES_MIN_LIFESPAN = 0.5
PARTICLES_MAX_LIFESPAN = 1

# Sounds
PADDLE_HIT = 'paddle-hit'
SCORE = 'score'
WALL_HIT = 'wall-hit'
CONFIRM = 'confirm'
SELECT = 'select'
NO_SELECT = 'no-select'
BRICK_HIT_1 = 'brick-hit-1'
BRICK_HIT_2 = 'brick-hit-2'
HURT = 'hurt'
VICTORY = 'victory'
RECOVER = 'recover'
HIGH_SCORE = 'high-score'
PAUSE = 'pause'

MUSIC = 'music'
GLOBAL_VOLUME = 0.3
MUSIC_VOLUME = 0.2

# States
START = 'start'
SERVE = 'serve'
PLAY = 'play'
GAME_OVER = 'game_over'
ENTER_HIGH_SCORE = 'enter_high_score'
PADDLE_SELECT = 'paddle_select'


# Game
PADDLE_SPEED = 200
BRICKS_PADDING = 8
LEFT_SIDE_PADDING = 16
BALL_BOUNCE_SPEED = 50
BALL_BOUNCE_FACTOR = 8
BALL_DY_FACTOR = 1.02
MAX_HEALTH = 3
TIER_MULT = 200
SKIN_MULT = 25
RECOVER_POINTS = 5000

# Frames
PADDLES = 'paddles'
BALLS = 'balls'
BRICKS = 'bricks'
HEART_FULL = 0
HEART_EMPTY = 1

# Physics
GRAVITY = np.array([0, -10])
PIXEL_SIZE = 20 / WIDTH

# UI
HIGH_SCORE_COUNT = 10
