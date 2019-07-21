from random import random, randint


class Agent:
    def __init__(self, world, state_start, epsilon=0.2, discount_factor=0.8,
                 learning_rate=0.1):
        self.state = state_start

        if epsilon < 0 or epsilon > 1:
            raise ValueError('Epsilon has to be in range [0...1]')
        self.epsilon = epsilon

        if discount_factor < 0 or discount_factor > 1:
            raise ValueError('Discount factor has to be in range [0...1]')
        self.discount_factor = discount_factor

        if learning_rate < 0 or learning_rate > 1:
            raise ValueError('Learning rate has to be in range [0...1]')
        self.learning_rate = learning_rate

        h, w = world.get_size()
        self.q = [{}] * h * w
        # q table initialization
        for i in range(0, h):
            for j in range(0, w):
                for a in world.states[i * world.width + j].actions.values():
                    self.q[i * world.width + j][a.name] = 0

    def get_best_action(self, state):
        actions = [a for a in state.actions.values()]
        best_action = actions[0]
        for i in range(1, len(actions)):
            w_pos = state.world_pos
            a_name = actions[i].name
            if self.q[w_pos][a_name] > self.q[w_pos][best_action.name]:
                best_action = actions[i]
        return best_action

    def q_update(self, action):
        state_new = action.state_new
        reward = state_new.reward
        best_action = self.get_best_action(state_new)

        w_pos = state_new.world_pos
        ba_name = best_action.name
        target_value = reward + self.discount_factor * self.q[w_pos][ba_name]
        average_update = self.q[self.state.world_pos][action.name] * \
            (1 - self.learning_rate) + target_value * self.learning_rate

        self.q[self.state.world_pos][action.name] = average_update

    def step(self):
        if random() < self.epsilon:
            action = [a for a in self.state.actions.values()]\
                [randint(0, len(self.state.actions) - 1)]
        else:
            action = self.get_best_action(self.state)

        self.q_update(action)
