from .Action import Action
from .State import State
from .Agent import Agent
from random import random


class World:
    def __init__(self, width, height, gamma=0.01, d_rate=0.8):
        self.width = width
        self.height = height
        self.states = [None] * width * height
        self.agent = None
        self.gamma = gamma
        self.d_rate = d_rate

        def yx(y, x): return y * self.width + x

        def spawn_cell_opened(y, x):
            # initially reward is -1, so agent looses reward while moving
            self.states[yx(y, x)] = State({
                'up': Action('up'),
                'down': Action('down'),
                'left': Action('left'),
                'right': Action('right')
            }, yx(y, x), -1)

        def spawn_cell_limited(y, x, actions_allowed):
            actions = {}
            for name in actions_allowed:
                actions[name] = Action(name)
            self.states[yx(y, x)] = State(actions, yx(y, x), -1)

        # generating states
        # middle ones
        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                spawn_cell_opened(i, j)

        # on the sides
        for i in range(1, self.height - 1):
            spawn_cell_limited(i, 0, ['up', 'down', 'right'])
            spawn_cell_limited(i, self.width - 1, ['up', 'down', 'left'])
        for j in range(1, self.width - 1):
            spawn_cell_limited(0, j, ['down', 'left', 'right'])
            spawn_cell_limited(self.height - 1, j, ['up', 'left', 'right'])

        # corners
        spawn_cell_limited(0, 0, ['down', 'right'])
        spawn_cell_limited(0, self.width - 1, ['down', 'left'])
        spawn_cell_limited(self.height - 1, 0, ['up', 'right'])
        spawn_cell_limited(self.height - 1, self.width - 1, ['up', 'left'])

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
        self.add_agent()

    def get_size(self):
        return self.width, self.height

    def randomize_reward(self):
        for s in self.states:
            s.reward = random()

    def value_iteration(self):
        for s in self.states:
            actions = [a for a in s.actions]
            best_neighbour = actions[0]
            for a in range(1, len(actions)):
                if actions[a].state_new.value > best_neighbour.value:
                    best_neighbour = actions[a].state_new

            s.value = s.reward + self.d_rate * best_neighbour.value

    def add_agent(self, state=None):
        if state is None:
            state = self.states[0]
        agent = Agent(self, state)
        self.agent = agent
        return agent
