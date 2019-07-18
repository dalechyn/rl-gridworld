class Agent:
    def __init__(self, world):
        self.q = []
        h, w = world.get_size()
        # q table initialization
        for i in range(0, h):
            self.q.append([])
            for j in range(0, w):
                self.q[i].append({})
                for a in world.actions:
                    self.q[i][j][a.name] = 0

