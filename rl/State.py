class State:
    def __init__(self, actions, reward=0):
        self.reward = reward
        self.actions = actions

    def get_actions(self):
        return self.actions
