class BaseState:
    def __init__(self, state_machine):
        self.state_machine = state_machine

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, dt):
        pass

    def render(self):
        pass
