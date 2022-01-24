from pyglet.text import Label
from pyglet.window import key


from constants import *
from states import BaseState


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

    def enter(self, score=0):
        self.score_label.text = FINAL_SCORE_STR.format(score)

    def render(self):
        self.label.draw()
        self.score_label.draw()
        self.press_enter_label.draw()

    def on_key_press(self, symbol):
        if symbol == key.ENTER or symbol == key.RETURN:
            self.state_machine.change(START)
