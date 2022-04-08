import logging
import sys
import time
from collections import defaultdict
from pathlib import Path

import seaborn

from src.config import Config
from src.displayer import Displayer
from src.map import create_map
from src.role import Role, RandomRole, StayRole, GeneticPolice, AStarPolice
from src.role import Action

import numpy as np
import pygame as pg
import pandas as pd

from pygame.locals import *

from src.status import Status


class QLearning:
    def __init__(self, action_space, actions, epsilon):
        self.actions = actions
        self.alpha = 0.5
        self.gamma = 0.9
        self.epsilon = epsilon
        self.actions = actions
        self.q_table = defaultdict(lambda: np.zeros(action_space))

    def set_q_table(self, q_table):
        self.q_table = q_table

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
            self.epsilon -= 0.0001
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
    def __init__(self, actions, epsilon):
        super().__init__()
        self._action_space = [Action.Stay, Action.Up, Action.Down, Action.Left, Action.Right]
        self._n_actions = len(self._action_space)
        self._q_learning = QLearning(self._n_actions, actions, epsilon)

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


def create_s_q_roles():
    thief = StayRole()
    thief.move((0, 9))
    police = QLearningThief(list(range(5)), epsilon=0.3)
    police.move((24, 0))
    return thief, police


def create_r_a_roles(map, heuristic):
    thief = RandomRole()
    thief.move((0, 9))
    police = AStarPolice(map, heuristic)
    police.move((24, 0))
    return thief, police


def create_q_g_roles(map):
    thief = QLearningThief(list(range(5)), epsilon=0.1)
    thief.move((0, 9))
    police = GeneticPolice(map, num_iteration=10, mutation_rate=0.1)
    police.move((24, 0))
    return thief, police


def create_q_a_roles(map, heuristic):
    thief = QLearningThief(list(range(5)), epsilon=0.01)
    thief.move((0, 9))
    police = AStarPolice(map, heuristic)
    police.move((24, 0))
    return thief, police


def create_q_r_roles():
    thief = QLearningThief(list(range(5)), epsilon=0.1)
    thief.move((0, 9))
    police = RandomRole()
    police.move((24, 0))
    return thief, police


def create_r_g_roles(map):
    thief = RandomRole()
    thief.move((0, 9))
    police = GeneticPolice(map, num_iteration=100, mutation_rate=0.3)
    police.move((24, 0))
    return thief, police


def execute_q(status, thief, police, iteration):
    police_current_pos = status.police.pos
    if iteration > 100:
        police.move(police.get_action(status).dest(police.pos))
        status.new_step()
        police_next_pos = status.police.pos
    else:
        police_next_pos = status.police.pos

    thief_current_pos = status.thief.pos
    thief_action = thief.get_action(status)
    thief_next_pos = thief_action.dest(thief.pos)
    if not status.map.valid(thief_next_pos):
        return -100
    reward = status.get_reward("thief", (thief_current_pos, thief_next_pos), (police_current_pos, police_next_pos))
    thief.q_learning.learn(thief_current_pos, thief_action, reward, thief_next_pos)
    if status.map.wall(thief_next_pos):
        return -100
    thief.move(thief_next_pos)
    status.thief.pos = thief_next_pos
    return reward


def execute_s_q(status, police):
    police_current_pos = status.police.pos
    police_action = police.get_action(status)
    police_next_pos = police_action.dest(police.pos)

    print("action:", police_action)

    if not status.map.valid(police_next_pos):
        return -100
    reward = status.get_reward("police", ((0, 9), (0, 9)), (police_current_pos, police_next_pos))
    police.q_learning.learn(police_current_pos, police_action, reward, police_next_pos)
    if status.map.wall(police_next_pos):
        return -100
    police.move(police_next_pos)
    status.new_step()
    status.police.pos = police_next_pos
    return reward


def execute_r_g(status, thief, police, iteration):
    thief.move(thief.get_action(status).dest(thief.pos))
    if iteration > 100:
        police.move(police.get_action(status).dest(police.pos))
        status.new_step()


def plot_q_table(map, police):
    file = np.empty([map.height, map.width])
    file[:] = np.nan
    for k, v in police.q_learning.q_table.items():
        if isinstance(k, tuple):
            file_action = list(v).index(max(list(v)))
            file[k[1], k[0]] = file_action
    for i in range(map.height):
        for j in range(map.width):
            if map.wall([j, i]):
                file[i, j] = -100
    arr = np.array(file)
    df = pd.DataFrame(data=arr)
    df.to_csv("q-table.csv")


def main():
    over_step = 0
    eposides = 3
    record_q_table = defaultdict(lambda: np.zeros(5))

    for eposide in range(eposides):
        pg.init()
        pg.display.set_caption("Chase AI")
        cfg = Config()
        cfg.load(Path(__file__).parent.joinpath("config.json"))

        map = create_map("senior")
        # thief, police = create_q_r_roles()
        # thief, police = create_s_q_roles()
        # thief, police = create_r_g_roles(map)
        # thief, police = create_q_g_roles(map)
        # thief, police = create_r_a_roles(map, cfg.heuristic)
        thief, police = create_q_a_roles(map, cfg.heuristic)
        status = Status()
        status.map = map
        status.step = 0
        status.thief = thief
        status.police = police

        # when use inherit q table
        thief.q_learning.set_q_table(record_q_table)

        iteration = 0

        displayer = Displayer(map, status, cfg.fps)
        while True:
            iteration = iteration + 1
            for event in pg.event.get():
                if event.type == QUIT:
                    plot_q_table(status.map, status.thief)
                    pg.quit()
                    sys.exit()
            if not status.game_end():
                reward = execute_q(status, thief, police, iteration)
                # reward = execute_r_g(status, thief, police, iteration)
                # reward = execute_s_q(status, police)
                print(reward)

                displayer.update()
            else:
                plot_q_table(status.map, status.thief)
                print(f"The game ended with {status.step} steps.")
                break
        # when use inherit q table
        record_q_table = thief.q_learning.q_table
        over_step = over_step + status.step
    print(f"mean step: {over_step / eposides} ")


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
