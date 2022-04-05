import logging
import sys
import time
from collections import defaultdict
from pathlib import Path

from src.config import Config
from src.displayer import Displayer
from src.main import create_map
from src.role import Role, RandomRole
from src.role import Action

import numpy as np
import pygame as pg
from pygame.locals import *

from src.status import Status


def create_q_r_roles():
    agent = QLearningAgent(list(range(5)))
    agent.move((0, 0))
    enemy = RandomRole()
    enemy.move((9, 9))
    return agent, enemy


def create_r_r_roles():
    agent = RandomRole()
    agent.move((0, 0))
    enemy = RandomRole()
    enemy.move((9, 9))
    return agent, enemy


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


class QLearningAgent(_QLearningRole):
    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value

    def _target(self, status):
        return status.thief


def execute_q(status, agent, enemy):
    enemy_current_pos = status.enemy.pos
    enemy.move(enemy.get_action(status).dest(enemy.pos))
    enemy_next_pos = status.enemy.pos

    agent_current_pos = status.agent.pos
    agent_action = agent.get_action(status)
    agent_next_pos = agent_action.dest(agent.pos)
    if status.map.wall(agent_next_pos):
        return 0
    agent.move(agent_next_pos)
    # print(thief_next_pos)
    reward = status.get_reward((agent_current_pos, agent_next_pos), (enemy_current_pos, enemy_next_pos))
    agent.q_learning.learn(agent_current_pos, agent_action, reward, agent_next_pos)
    status.agent.pos = agent_next_pos
    return reward


def execute_r(status, agent, enemy):
    agent.move(agent.get_action(status).dest(agent.pos))
    enemy.move(enemy.get_action(status).dest(enemy.pos))


def main():
    pg.init()
    pg.display.set_caption("Chase AI")

    cfg = Config()
    cfg.load(Path(__file__).parent.joinpath("config.json"))

    map = create_map()
    agent, enemy = create_q_r_roles()
    # agent, enemy = create_r_r_roles()
    score = 0
    status = Status()
    status.map = map
    status.agent = agent
    status.enemy = enemy

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
            reward = execute_q(status, agent, enemy)
            score = score + reward
            print(score)
            # execute_r(status, agent, enemy)
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
