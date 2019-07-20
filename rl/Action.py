class Action:
    def __init__(self, name):
        self.name = name
        self.state_old = None
        self.state_new = None

    def link(self, state_new, state_old):
        self.state_new = state_new
        self.state_old = state_old
