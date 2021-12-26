from base_state import BaseState


class StateMachine:
    def __init__(self, states=None):
        if states is None:
            states = {}
        self.states = states
        self.current = BaseState()

    def change(self, state_name):
        assert(state_name in self.states)
        self.current.exit()
        self.current = self.states[state_name]
        self.current.enter()

    def update(self, dt):
        self.current.update(dt)

    def render(self):
        self.current.render()
