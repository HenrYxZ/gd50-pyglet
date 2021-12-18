import pyglet
from pyglet import shapes
from pyglet.window import key

# Local Modules
from ball import Ball, BALL_W, BALL_H
from game import Game, PLAYER_1, PLAYER_2
import game
from paddle import Paddle

WIDTH = 800
HEIGHT = 600
COLOR_WHITE = (250, 250, 250)
COLOR_FPS = (0, 255, 0, 100)
FREQUENCY = 60.0
P1_X = 20
P1_Y = 20
p1 = Paddle(P1_X, P1_Y, HEIGHT)
P2_X = WIDTH - P1_X - p1.REC_W
P2_Y = HEIGHT - P1_Y - p1.REC_H
p2 = Paddle(P2_X, P2_Y, HEIGHT)
ball = Ball((WIDTH - BALL_W) / 2, (HEIGHT - BALL_H) / 2, WIDTH, HEIGHT)
current_game = Game()

window = pyglet.window.Window(WIDTH, HEIGHT, caption='Pong')
keys = key.KeyStateHandler()
window.push_handlers(keys)
# Load font
pyglet.font.add_file('font.ttf')
PONG_FONT_NAME = '04b03'
pong_font = pyglet.font.load(PONG_FONT_NAME)
# Labels
label = pyglet.text.Label(
    'Press ENTER to start!',
    font_name=PONG_FONT_NAME,
    font_size=28,
    x=80, y=40
)
p1_score_label = pyglet.text.Label(
    '0',
    font_name=PONG_FONT_NAME,
    font_size=46,
    x=160, y=HEIGHT / 2, anchor_x='center', anchor_y='center'
)
p2_score_label = pyglet.text.Label(
    '0',
    font_name=PONG_FONT_NAME,
    font_size=46,
    x=WIDTH - 160, y=HEIGHT / 2, anchor_x='center', anchor_y='center'
)
winner_label = pyglet.text.Label(
    font_name=PONG_FONT_NAME,
    font_size=36,
    x=80, y=HEIGHT - 60, anchor_x='center', anchor_y='center'
)
fps_label = pyglet.text.Label(
    color=COLOR_FPS, font_name=PONG_FONT_NAME, font_size=26
)
fps_display = pyglet.window.FPSDisplay(window)
fps_display.label = fps_label
# Load sounds
PADDLE_HIT = 'paddle_hit'
SCORE = 'score'
WALL_HIT = 'wall_hit'
sounds = {
    PADDLE_HIT: pyglet.media.load('sounds/paddle_hit.wav', streaming=False),
    SCORE: pyglet.media.load('sounds/score.wav', streaming=False),
    WALL_HIT: pyglet.media.load('sounds/wall_hit.wav', streaming=False)
}


def handle_input():
    # input for player 1
    if keys[key.W]:
        p1.v = p1.SPEED
    elif keys[key.S]:
        p1.v = -p1.SPEED
    else:
        p1.v = 0
    # input for player 2
    if keys[key.UP]:
        p2.v = p2.SPEED
    elif keys[key.DOWN]:
        p2.v = -p2.SPEED
    else:
        p2.v = 0


def handle_score(player_number):
    serving_number = PLAYER_2 if player_number == PLAYER_1 else PLAYER_1
    ball.reset(serving_number)
    current_game.state = game.SERVING_STATE
    current_game.serve = serving_number
    current_game.scores[player_number] += 1
    player_score = current_game.scores[player_number]
    score_lbl = p1_score_label if player_number == PLAYER_1 else p2_score_label
    score_lbl.text = f"{player_score}"
    # Check win
    if player_score == 10:
        current_game.winner = player_number
        current_game.state = game.DONE_STATE
        winner_label.text = f"Player {player_number} won!"
    player = sounds[SCORE].play()
    player.volume = 0.1


def handle_wall_hit(new_y):
    ball.y = new_y
    ball.dy = -ball.dy
    player = sounds[WALL_HIT].play()
    player.volume = 0.3


def handle_paddle_hit(new_x):
    ball.x = new_x
    ball.horizontal_bounce()
    player = sounds[PADDLE_HIT].play()
    player.volume = 0.3


def update(dt):
    if current_game.state == game.PLAYING_STATE:
        handle_input()
        p1.update(dt)
        p2.update(dt)
        ball.update(dt)
        # check collisions
        # with paddles
        if ball.collides(p1):
            handle_paddle_hit(p1.right)
        elif ball.collides(p2):
            handle_paddle_hit(p2.left - BALL_W)
        # with vertical boundaries
        if ball.y < 0:
            handle_wall_hit(0)
        elif ball.y > HEIGHT:
            handle_wall_hit(HEIGHT - BALL_H)
        # Check goal
        if ball.x < 0:
            handle_score(PLAYER_2)
        elif ball.x > WIDTH:
            handle_score(PLAYER_1)


def draw_player(player):
    shapes.Rectangle(
        x=player.x,
        y=player.y,
        width=player.REC_W,
        height=player.REC_H,
        color=COLOR_WHITE
    ).draw()


def draw_ball():
    shapes.Rectangle(
        x=ball.x,
        y=ball.y,
        width=BALL_W,
        height=BALL_H,
        color=COLOR_WHITE
    ).draw()


# Events Handling
# ------------------------------------------------------------------------------

@window.event
def on_draw():
    window.clear()
    draw_player(p1)
    draw_player(p2)
    draw_ball()
    if current_game.state != game.PLAYING_STATE:
        label.draw()
    fps_display.draw()
    p1_score_label.draw()
    p2_score_label.draw()
    if current_game.state == game.DONE_STATE:
        winner_label.draw()


def handle_pause(symbol, _):
    if symbol == key.ENTER:
        if current_game.state == game.PLAYING_STATE:
            current_game.state = game.PAUSE_STATE
        else:
            if current_game.state == game.DONE_STATE:
                current_game.reset()
            current_game.state = game.PLAYING_STATE


if __name__ == '__main__':
    window.push_handlers(on_key_press=handle_pause)
    pyglet.clock.schedule_interval(update, 1 / FREQUENCY)
    pyglet.app.run()
