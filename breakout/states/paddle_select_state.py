from pyglet.sprite import Sprite
from pyglet.text import Label
from pyglet.window import key


from breakout.constants import *
from breakout.level_maker import LevelMaker
from breakout.paddle import Paddle
from breakout import resources
from breakout.states import BaseState
from breakout import utils


class PaddleSelectState(BaseState):
    def __init__(self, *args):
        super(PaddleSelectState, self).__init__(*args)
        self.currentPaddle = 1
        self.high_scores = {}
        self.main_label = Label(
            "Select your paddle with left and right!", x=WIDTH/2, y=3*HEIGHT/4,
            font_name=FONT_NAME, font_size=MEDIUM, anchor_x='center',
            anchor_y='center'
        )
        self.instructions = Label(
            "(Press enter to continue!)", x=WIDTH/2, y=2*HEIGHT/3,
            font_name=FONT_NAME, font_size=SMALL, anchor_x='center',
            anchor_y='center'
        )
        self.arrow_left = Sprite(
            resources.frames[ARROWS][0], x=WIDTH/4-24, y=HEIGHT/3
        )
        self.arrow_right = Sprite(
            resources.frames[ARROWS][1], x=3*WIDTH/4, y=HEIGHT/3
        )
        self.paddle = Sprite(
            resources.frames[PADDLES][2+4*(self.currentPaddle-1)], x=WIDTH/2-32,
            y=HEIGHT/3
        )

    def enter(self, high_scores=None):
        self.high_scores = high_scores

    def render(self):
        self.main_label.draw()
        self.instructions.draw()
        self.paddle.draw()
        self.arrow_left.draw()
        self.arrow_right.draw()

    def on_key_press(self, symbol):
        if symbol == key.LEFT:
            if self.currentPaddle == 1:
                utils.play(resources.sounds[NO_SELECT])
            else:
                self.currentPaddle -= 1
                utils.play(resources.sounds[SELECT])
                self.paddle.image = (
                    resources.frames[PADDLES][2 + 4 * (self.currentPaddle - 1)]
                )
        elif symbol == key.RIGHT:
            if self.currentPaddle == 4:
                utils.play(resources.sounds[NO_SELECT])
            else:
                self.currentPaddle += 1
                utils.play(resources.sounds[SELECT])
                self.paddle.image = (
                    resources.frames[PADDLES][2 + 4 * (self.currentPaddle - 1)]
                )
        if self.currentPaddle == 1:
            self.arrow_left.color = (40, 40, 40)
            self.arrow_left.opacity = 128
        elif 1 < self.currentPaddle < 4:
            self.arrow_left.color = (255, 255, 255)
            self.arrow_left.opacity = 255
            self.arrow_right.color = (255, 255, 255)
            self.arrow_right.opacity = 255
        else:
            self.arrow_right.color = (40, 40, 40)
            self.arrow_right.opacity = 128

        if symbol == key.ENTER or symbol == key.RETURN:
            utils.play(resources.sounds[CONFIRM])
            self.state_machine.change(
                SERVE,
                level=1,
                paddle=Paddle(self.currentPaddle),
                bricks=LevelMaker.create_map(1),
                health=MAX_HEALTH,
                score=0,
                high_scores=self.high_scores,
            )
