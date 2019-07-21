class State:
    def __init__(self, actions, world_pos, reward=0):
        self.reward = reward
        self.actions = actions
        self.world_pos = world_pos
        self.value = 0

    def __repr__(self):
        return '<State>: {\n\t\t' + \
               ''.join([a.__repr__() + '\n\t\t' for a in self.actions]) + '}\n'

    def link(self, dr, state):
        self.actions[dr].state_old = self
        self.actions[dr].state_new = state
