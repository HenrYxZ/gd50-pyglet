import pyglet
from pyglet.window import key


from constants import *
from paddle import Paddle
from level_maker import LevelMaker
from states import BaseState
from resources import sounds
import utils


class StartState(BaseState):
    def __init__(self, *args):
        super().__init__(*args)
        self.highlighted = 1
        self.high_scores = {}
        self.batch = pyglet.graphics.Batch()
        self.title_label = pyglet.text.Label(
            "BREAKOUT", x=WIDTH/2, y=HEIGHT-HEIGHT/3, font_name=FONT_NAME,
            font_size=LARGE, batch=self.batch, anchor_x='center',
            anchor_y='center'
        )
        self.start_label = pyglet.text.Label(
            "START", x=WIDTH/2, y=HEIGHT-(HEIGHT/2+70), font_name=FONT_NAME,
            font_size=MEDIUM, batch=self.batch, anchor_x='center',
            anchor_y='center'
        )
        self.scores_label = pyglet.text.Label(
            "HIGH SCORES", x=WIDTH/2, y=HEIGHT-(HEIGHT/2+90),
            font_name=FONT_NAME,
            font_size=MEDIUM, batch=self.batch, anchor_x='center',
            anchor_y='center'
        )

    def enter(self, high_scores):
        self.high_scores = high_scores

    def on_key_press(self, symbol):
        if symbol == key.UP or symbol == key.DOWN:
            self.highlighted = 2 if self.highlighted == 1 else 1
            utils.play(sounds[PADDLE_HIT])
        if symbol == key.ENTER or symbol == key.RETURN:
            if self.highlighted == 1:
                self.state_machine.change(
                    SERVE,
                    level=1,
                    paddle=Paddle(1),
                    bricks=LevelMaker.create_map(1),
                    health=MAX_HEALTH,
                    score=0,
                    high_scores=self.high_scores
                )
                utils.play(sounds[CONFIRM])
            else:
                self.state_machine.change(
                    HIGH_SCORE,
                    high_scores=self.high_scores
                )

    def render(self):
        if self.highlighted == 1:
            self.start_label.color = COLOR_HIGHLIGHTED
            self.scores_label.color = WHITE
        else:
            self.start_label.color = WHITE
            self.scores_label.color = COLOR_HIGHLIGHTED
        self.batch.draw()
