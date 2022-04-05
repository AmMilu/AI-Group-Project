import math


def e_disdance(x, y):
    return math.sqrt(sum(pow(a - b, 2) for a, b in zip(x, y)))


def m_disdance(x, y):
    return sum(abs(a - b) for a, b in zip(x, y))


class Status:
    def __init__(self):
        self.agent = None
        self.enemy = None
        self.map = None

    def game_end(self):
        return self.agent.pos == self.enemy.pos

    def get_reward(self, agent, enemy):
        if self.map.wall(agent[1]):
            reward = -100
        else:
            old_distance = e_disdance(enemy[0], agent[0])
            new_distance = e_disdance(enemy[1], agent[1])
            reward = new_distance - old_distance
        return reward
