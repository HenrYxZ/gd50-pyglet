from base_state import BaseState


class StateMachine:
    def __init__(self, states=None):
        """
        A state machine.
        Args:
            states: A list of functions to create each kind of state

        Attributes:
            states: A list of functions to create each kind of state
            current: The current state of the machine as a State object
        """
        if states is None:
            states = {}
        self.states = states
        self.current = BaseState()

    def change(self, state_name, **kwargs):
        assert(state_name in self.states)
        self.current.exit()
        self.current = self.states[state_name]()
        self.current.enter(**kwargs)

    def update(self, dt):
        self.current.update(dt)

    def render(self):
        self.current.render()
