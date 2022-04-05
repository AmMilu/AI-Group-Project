import logging
import sys
import time
from collections import defaultdict
from pathlib import Path

from src.config import Config
from src.displayer import Displayer
from src.main import create_map
from src.role import Role, RandomRole, StayRole, GeneticPolice
from src.role import Action

import numpy as np
import pygame as pg
from pygame.locals import *

from src.status import Status


def create_s_q_roles():
    thief = StayRole()
    thief.move((0, 0))
    police = QLearningThief(list(range(5)))
    police.move((24, 0))
    return thief, police


def create_r_r_roles():
    thief = RandomRole()
    thief.move((0, 0))
    police = RandomRole()
    police.move((24, 0))
    return thief, police


def create_q_g_roles(map):
    thief = QLearningThief(list(range(5)))
    thief.move((0, 0))
    police = GeneticPolice(map)
    police.move((24, 0))
    return thief, police


def create_q_r_roles():
    thief = QLearningThief(list(range(5)))
    thief.move((0, 0))
    police = RandomRole()
    police.move((24, 0))
    return thief, police


class QLearning:
    def __init__(self, action_space, actions):
        self.actions = actions
        self.alpha = 0.1
        self.gamma = 0.85
        self.epsilon = 0.01
        self.actions = actions
        self.q_table = defaultdict(lambda: np.zeros(action_space))

    def get_action(self, state):
        if np.random.uniform() > self.epsilon:
            action_values = self.q_table[state]
            argmax_actions = []
            for i in range(len(action_values)):
                if action_values[i] == np.max(action_values):
                    argmax_actions.append(i)
            next_action = np.random.choice(argmax_actions)
        else:
            next_action = np.random.choice(self.actions)
        if self.epsilon > 0:
            self.epsilon -= 0.00001
        if self.epsilon < 0:
            self.epsilon = 0

        return next_action

    def learn(self, current_state, current_action, reward, next_state):
        next_action = np.argmax(self.q_table[next_state])
        new_q = reward + self.gamma * self.q_table[next_state][int(next_action)]
        self.q_table[current_state][current_action] = (1 - self.alpha) * self.q_table[current_state][
            current_action] + self.alpha * new_q


class _QLearningRole(Role):
    # role use q_learning
    def __init__(self, actions):
        super().__init__()
        self._action_space = [Action.Stay, Action.Up, Action.Down, Action.Left, Action.Right]
        self._n_actions = len(self._action_space)
        self._q_learning = QLearning(self._n_actions, actions)

    def get_action_value(self, status):
        return self._q_learning.get_action(status)

    def get_action(self, status):
        value = self._q_learning.get_action(status)
        return Action.next_(value)

    def _target(self, status):
        assert False

    def q_learning(self):
        return self._q_learning

    @property
    def q_learning(self):
        return self._q_learning


class QLearningThief(_QLearningRole):
    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value

    def _target(self, status):
        return status.thief


def execute_q(status, thief, police):
    police_current_pos = status.police.pos
    police.move(police.get_action(status).dest(police.pos))
    police_next_pos = status.police.pos

    thief_current_pos = status.thief.pos
    thief_action = thief.get_action(status)
    thief_next_pos = thief_action.dest(thief.pos)
    if status.map.wall(thief_next_pos):
        return 0
    thief.move(thief_next_pos)
    # print(thief_next_pos)
    reward = status.get_reward((thief_current_pos, thief_next_pos), (police_current_pos, police_next_pos))
    thief.q_learning.learn(thief_current_pos, thief_action, reward, thief_next_pos)
    status.thief.pos = thief_next_pos
    return reward


def execute_s_q(status, thief, police):
    police_current_pos = status.police.pos
    police_action = police.get_action(status)
    police_next_pos = police_action.dest(police.pos)
    if status.map.wall(police_next_pos):
        return 0
    police.move(police_next_pos)
    reward = -status.get_reward(((0, 0), (0, 0)), (police_current_pos, police_next_pos))
    police.q_learning.learn(police_current_pos, police_action, reward, police_next_pos)
    status.police.pos = police_next_pos
    return reward


def execute_r(status, thief, police):
    thief.move(thief.get_action(status).dest(thief.pos))
    police.move(police.get_action(status).dest(police.pos))

def main():
    pg.init()
    pg.display.set_caption("Chase AI")

    cfg = Config()
    cfg.load(Path(__file__).parent.joinpath("config.json"))

    map = create_map()
    # thief, police = create_q_r_roles()
    # thief, police = create_r_r_roles()
    # thief, police = create_s_q_roles()
    thief, police = create_q_g_roles(map)
    score = 0
    status = Status()
    status.map = map
    status.thief = thief
    status.police = police

    displayer = Displayer(map, status, cfg.fps)

    start_time = time.time()
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                end_time = time.time()
                print(end_time - start_time)  # Training dodge: random 17.1183 q_learning 152.7683
                pg.quit()
                sys.exit()
        if not status.game_end():
            # reward = execute_q(status, thief, police)
            # score = score + reward
            # print(score)

            # execute_r(status, thief, police)

            reward = execute_q(status, thief, police)
            score = score + reward
            print(score)

        displayer.update()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    try:
        main()
    except SystemExit:
        pass
    except BaseException as err:
        logger.exception(err)
        sys.exit(1)
