START_STATE = "start"
PAUSE_STATE = "pause"
PLAYING_STATE = "playing"
SERVING_STATE = "serving"
DONE_STATE = "done"
PLAYER_1 = 1
PLAYER_2 = 2

class Game:
    def __init__(self):
        self.scores = {PLAYER_1: 0, PLAYER_2: 0}
        self.state = START_STATE
        self.serve = PLAYER_1
        self.winner = PLAYER_1

    def reset(self):
        self.scores = {PLAYER_1: 0, PLAYER_2: 0}
