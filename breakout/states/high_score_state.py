import pyglet
from pyglet.text import Label
from pyglet.window import key


from constants import *
from states import BaseState
from resources import sounds
import utils


class HighScoreState(BaseState):
    def __init__(self, *args):
        super().__init__(*args)
        self.high_scores = {}
        self.batch = pyglet.graphics.Batch()
        Label(
            "High Scores", x=WIDTH/2, y=HEIGHT-20, font_name=FONT_NAME,
            font_size=LARGE, anchor_x='center', anchor_y='center',
            batch=self.batch
        )
        Label(
            "Press Enter to return to the main menu!", x=WIDTH/2, y=18,
            font_name=FONT_NAME, font_size=SMALL, anchor_x='center',
            anchor_y='center', batch=self.batch
        )

    def enter(self, high_scores):
        self.high_scores = high_scores
        x0 = WIDTH / 4 - 38
        x1 = WIDTH / 4 + 38 + 50
        x2 = WIDTH / 2 + 150
        for row_num in self.high_scores.keys():
            y = HEIGHT - (60 + row_num * 15)
            row = self.high_scores[row_num]

            Label(
                f"{row_num}.", x=x0, y=y, font_name=FONT_NAME,
                font_size=MEDIUM, anchor_x='left',
                batch=self.batch
            )
            Label(
                row["name"], x=x1, y=y, font_name=FONT_NAME,
                font_size=MEDIUM, anchor_x='right',
                batch=self.batch
            )
            Label(
                str(row["score"]), x=x2, y=y, font_name=FONT_NAME,
                font_size=MEDIUM, anchor_x='right',
                batch=self.batch
            )

    def on_key_press(self, symbol):
        if symbol == key.ENTER or symbol == key.RETURN:
            self.state_machine.change(
                START,
                high_scores=self.high_scores
            )
            utils.play(sounds[WALL_HIT])

    def render(self):
        self.batch.draw()
