from pyglet.text import Label


from constants import *
from resources import frames


HEARTS_OFFSET = 11
SCORE_STR = 'Score: {0}'


score_label = Label(
    SCORE_STR, font_name=FONT_NAME, font_size=SMALL, x=WIDTH-60, y=5
)


def render_health(health):
    x = WIDTH - 100
    y = HEIGHT - 13

    for i in range(health):
        frames[HEARTS][HEART_FULL].blit(x, y)
        x += HEARTS_OFFSET

    for i in range(MAX_HEALTH - health):
        frames[HEARTS][HEART_EMPTY].blit(x, y)
        x += HEARTS_OFFSET


def render_score(score):
    score_label.text = SCORE_STR.format(score)
    score_label.draw()
