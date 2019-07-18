from .Action import Action
from .State import State

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.states = []
        self.actions = []

    def get_size(self):
        return self.width, self.height

    def build_gridworld(self):
        self.actions = [Action('up'), Action('down'),
                         Action('left'), Action('right')]

        def cell_opened():
            return State([Action('up'), Action('down'),
                         Action('left'), Action('right')], -1)

        def cell_blocked(actions_blocked):
            cell = cell_opened()
            cell.actions = [cell.actions.remove(a) for a in actions_blocked]
            return cell

        # generating states
        for i in range(0, self.height):
            for j in range(0, self.width):
                # initially reward is -1, so agent looses reward while moving
                self.states.append(cell_opened())

