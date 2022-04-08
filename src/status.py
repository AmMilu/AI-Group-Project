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

    def get_reward(self, role, thief, police):
        if role == "police" and self.map.wall(police[1]):
            return -100
        if role == "thief" and self.map.wall(thief[1]):
            return -100

        if self.game_end():
            return -100
        else:
            if role == "thief":
                old_distance = m_disdance(police[0], thief[0])
                new_distance = m_disdance(police[1], thief[1])
                reward = new_distance - old_distance
                return reward
            if role == "police":
                left_distance = m_disdance((0, 9), police[1])
                right_distance = m_disdance((24, 0), police[1])
                reward = right_distance - left_distance + 33
                return reward

    def new_step(self):
        self.step += 1
