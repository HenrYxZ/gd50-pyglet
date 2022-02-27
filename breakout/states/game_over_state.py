from pyglet.text import Label
from pyglet.window import key


from constants import *
from breakout.states import BaseState


FINAL_SCORE_STR = "Final Score: {0}"


class GameOverState(BaseState):
    def __init__(self, *args, **kwargs):
        super(GameOverState, self).__init__(*args, **kwargs)
        self.label = Label(
            "GAME OVER", font_name=FONT_NAME, font_size=LARGE, x=WIDTH/2,
            y=2*HEIGHT/3, anchor_x='center', anchor_y='center'
        )
        self.score_label = Label(
            "", font_name=FONT_NAME, font_size=MEDIUM,
            x=WIDTH/2, y=HEIGHT/2, anchor_x='center', anchor_y='center'
        )
        self.press_enter_label = Label(
            "Press Enter!", font_name=FONT_NAME, font_size=MEDIUM, x=WIDTH/2,
            y=HEIGHT/4, anchor_x='center', anchor_y='center'
        )
        self.score = 0
        self.high_scores = {}

    def enter(self, score=0, high_scores=None):
        self.score_label.text = FINAL_SCORE_STR.format(score)
        self.score = score
        self.high_scores = high_scores

    def render(self):
        self.label.draw()
        self.score_label.draw()
        self.press_enter_label.draw()

    def on_key_press(self, symbol):
        if symbol == key.ENTER or symbol == key.RETURN:
            n = len(self.high_scores.keys())
            high_score = False
            score_idx = n + 1
            for i in range(n):
                counter = i + 1
                if self.score > self.high_scores[counter]["score"]:
                    high_score = True
                    score_idx = counter
                    break
            if high_score:
                self.state_machine.change(
                    ENTER_HIGH_SCORE,
                    high_scores=self.high_scores,
                    score=self.score,
                    score_idx=score_idx
                )
            else:
                self.state_machine.change(START, high_scores=self.high_scores)
