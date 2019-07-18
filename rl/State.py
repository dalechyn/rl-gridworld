class State:
    def __init__(self, actions, reward=0):
        self.reward = reward
        self.actions = actions

    def __repr__(self):
        return '<State>: {\n\t\t' + ''.join([a.__repr__() + '\n\t\t' for a in self.actions]) + '}\n'

    def link(self, dr, state):
        self.actions[dr].state_old = self
        self.actions[dr].state_new = state

    def get_action_by_name(self, name):
        for a in self.actions:
            if a.name == name:
                return a
        return None
