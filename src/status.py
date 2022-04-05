import math


def e_disdance(x, y):
    return math.sqrt(sum(pow(a - b, 2) for a, b in zip(x, y)))


def m_disdance(x, y):
    return sum(abs(a - b) for a, b in zip(x, y))


class Status:
    def __init__(self):
        self.thief = None
        self.police = None
        self.map = None
        self.step = 0

    def game_end(self):
        return self.thief.pos == self.police.pos

    def get_reward(self, thief, police):
        if self.map.wall(thief[1]):
            reward = -100
        else:
            old_distance = e_disdance(police[0], thief[0])
            new_distance = e_disdance(police[1], thief[1])
            reward = new_distance - old_distance
        return reward

    def new_step(self):
        self.step += 1
