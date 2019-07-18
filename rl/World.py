from .Action import Action
from .State import State


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.states = [None] * width * height
        self.actions = []

    def get_size(self):
        return self.width, self.height

    def build_gridworld(self):
        def cell_opened():
            # initially reward is -1, so agent looses reward while moving
            return State({
                'up': Action('up'),
                'down': Action('down'),
                'left': Action('left'),
                'right': Action('right')
            }, -1)

        def cell_allowed(actions_allowed):
            actions = {}
            for name in actions_allowed:
                actions[name] = Action(name)
            return State(actions, -1)

        def yx(y, x): return y * self.width + x

        # generating states
        # middle ones
        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                self.states[yx(i, j)] = cell_opened()

        # on the sides
        for i in range(1, self.height - 1):
            self.states[yx(i, 0)] = cell_allowed(['up', 'down', 'right'])
            self.states[yx(i, self.width - 1)] = cell_allowed(['up', 'down', 'left'])
        for j in range(1, self.width - 1):
            self.states[yx(0, j)] = cell_allowed(['down', 'left', 'right'])
            self.states[yx(self.height - 1, j)] = cell_allowed(['up', 'left', 'right'])

        # corners
        self.states[yx(0, 0)] = cell_allowed(['down', 'right'])
        self.states[yx(0, self.width - 1)] = cell_allowed(['down', 'left'])
        self.states[yx(self.height - 1, 0)] = cell_allowed(['up', 'right'])
        self.states[yx(self.height - 1, self.width - 1)] = cell_allowed(['up', 'left'])

        # connecting states between each other
        # the middle ones
        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                state_cur = self.states[yx(i, j)]
                state_cur.link('up', self.states[yx(i - 1, j)])
                state_cur.link('down', self.states[yx(i + 1, j)])
                state_cur.link('left', self.states[yx(i, j - 1)])
                state_cur.link('right', self.states[yx(i, j + 1)])

        # the side ones
        for i in range(1, self.height - 1):
            state_cur = self.states[yx(i, 0)]
            state_cur.link('up', self.states[yx(i - 1, 0)])
            state_cur.link('down', self.states[yx(i + 1, 0)])
            state_cur.link('right', self.states[yx(i, 1)])
            state_cur = self.states[yx(i, self.width - 1)]
            state_cur.link('up', self.states[yx(i - 1, self.width - 1)])
            state_cur.link('down', self.states[yx(i + 1, self.width - 1)])
            state_cur.link('left', self.states[yx(i, self.width - 2)])

        for j in range(1, self.width - 1):
            state_cur = self.states[yx(0, j)]
            state_cur.link('down', self.states[yx(1, j)])
            state_cur.link('left', self.states[yx(0, j - 1)])
            state_cur.link('right', self.states[yx(0, j + 1)])
            state_cur = self.states[yx(self.height - 1, j)]
            state_cur.link('up', self.states[yx(self.height - 2, j)])
            state_cur.link('left', self.states[yx(self.height - 1, j - 1)])
            state_cur.link('right', self.states[yx(self.height - 1, j + 1)])

        # and finally the corners
        state_cur = self.states[yx(0, 0)]
        state_cur.link('down', self.states[yx(1, 0)])
        state_cur.link('right', self.states[yx(0, 1)])
        state_cur = self.states[yx(0, self.width - 1)]
        state_cur.link('down', self.states[yx(1, self.width - 1)])
        state_cur.link('left', self.states[yx(0, self.width - 2)])
        state_cur = self.states[yx(self.height - 1, 0)]
        state_cur.link('up', self.states[yx(self.height - 2, 0)])
        state_cur.link('right', self.states[yx(self.height - 1, 1)])
        state_cur = self.states[yx(self.height - 1, self.width - 1)]
        state_cur.link('up', self.states[yx(self.height - 2, self.width - 1)])
        state_cur.link('left', self.states[yx(self.height - 1, self.width - 2)])
