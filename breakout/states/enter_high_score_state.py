import pyglet
from pyglet.text import Label
from pyglet.window import key


from constants import *
from states import BaseState
from resources import sounds
import utils


class EnterHighScoreState(BaseState):
    def __init__(self, *args):
        super().__init__(*args)
        self.highlighted = 1
        self.high_scores = {}
        self.score = 0
        self.score_idx = 0
        self.chars = {1: 65, 2: 65, 3: 65}
        self.batch = pyglet.graphics.Batch()
        y = HEIGHT / 2
        self.title_label = Label(
            x=WIDTH/2, y=HEIGHT-30, font_name=FONT_NAME,
            font_size=LARGE, batch=self.batch, anchor_x='center',
            anchor_y='center'
        )
        self.first_label = Label(
            chr(self.chars[1]), x=WIDTH/2-28, y=y, font_name=FONT_NAME,
            font_size=LARGE, batch=self.batch, anchor_x='center',
            anchor_y='center'
        )
        self.second_label = Label(
            chr(self.chars[2]), x=WIDTH/2-6, y=y, font_name=FONT_NAME,
            font_size=LARGE, batch=self.batch, anchor_x='center',
            anchor_y='center'
        )
        self.third_label = Label(
            chr(self.chars[1]), x=WIDTH/2+20, y=y,
            font_name=FONT_NAME,
            font_size=LARGE, batch=self.batch, anchor_x='center',
            anchor_y='center'
        )
        self.instructions = Label(
            "Press Enter to confirm!", x=WIDTH / 2, y=18,
            font_name=FONT_NAME, font_size=SMALL, batch=self.batch,
            anchor_x='center', anchor_y='center'
        )
        self.highlight()

    def enter(self, high_scores=None, score=0, score_idx=0):
        self.high_scores = high_scores
        self.score = score
        self.score_idx = score_idx
        self.title_label.text = f"Your score: {score}"

    def highlight(self):
        if self.highlighted == 1:
            self.first_label.color = COLOR_HIGHLIGHTED
            self.second_label.color = WHITE
            self.third_label.color = WHITE
        elif self.highlighted == 2:
            self.first_label.color = WHITE
            self.second_label.color = COLOR_HIGHLIGHTED
            self.third_label.color = WHITE
        else:
            self.first_label.color = WHITE
            self.second_label.color = WHITE
            self.third_label.color = COLOR_HIGHLIGHTED

    def get_label(self, label_number):
        if label_number == 1:
            return self.first_label
        elif label_number == 2:
            return self.second_label
        else:
            return self.third_label

    def update_scores(self):
        # Update rows from bottom-up getting the value from row above
        for row_num in range(10, self.score_idx, -1):
            self.high_scores[row_num] = {
                "name": self.high_scores[row_num - 1]["name"],
                "score": self.high_scores[row_num - 1]["score"]
            }

    def on_key_press(self, symbol):
        if symbol == key.UP:
            current_char = self.chars[self.highlighted]
            current_char += 1
            if current_char > 90:
                current_char = 65
            self.chars[self.highlighted] = current_char
            self.get_label(self.highlighted).text = chr(current_char)
        elif symbol == key.DOWN:
            current_char = self.chars[self.highlighted]
            current_char -= 1
            if current_char < 65:
                current_char = 90
            self.chars[self.highlighted] = current_char
            self.get_label(self.highlighted).text = chr(current_char)
        if symbol == key.LEFT:
            self.highlighted -= 1
            if self.highlighted < 1:
                self.highlighted = 3
            self.highlight()
        elif symbol == key.RIGHT:
            self.highlighted += 1
            if self.highlighted > 3:
                self.highlighted = 1
            self.highlight()
        if symbol == key.ENTER or symbol == key.RETURN:
            self.update_scores()
            self.high_scores[self.score_idx] = {
                "name": "".join(map(chr, self.chars.values())),
                "score": self.score
            }
            # Write high scores in disc
            utils.write_high_scores(self.high_scores)
            self.state_machine.change(HIGH_SCORE, high_scores=self.high_scores)

    def render(self):
        self.batch.draw()
