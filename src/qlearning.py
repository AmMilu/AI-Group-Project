import logging
import sys
import time
from collections import defaultdict
from pathlib import Path

from src.config import Config
from src.displayer import Displayer
from src.map import create_map
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
    police = GeneticPolice(map, num_iteration=10, mutation_rate=0.3)
    police.move((24, 0))
    return thief, police


def create_q_r_roles():
    thief = QLearningThief(list(range(5)))
    thief.move((0, 0))
    police = RandomRole()
    police.move((24, 0))
    return thief, police


def create_r_g_roles(map):
    thief = RandomRole()
    thief.move((0, 0))
    police = GeneticPolice(map, num_iteration=10, mutation_rate=0.3)
    police.move((24, 0))
    return thief, police


class QLearning:
    def __init__(self, action_space, actions):
        self.actions = actions
        self.alpha = 0.5
        self.gamma = 0.9
        self.epsilon = 0.3
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
    if status.map.wall(thief_next_pos):
        return 0
    thief.move(thief_next_pos)
    reward = status.get_reward((thief_current_pos, thief_next_pos), (police_current_pos, police_next_pos))
    thief.q_learning.learn(thief_current_pos, thief_action, reward, thief_next_pos)
    status.thief.pos = thief_next_pos


def execute_s_q(status, police):
    police_current_pos = status.police.pos
    police_action = police.get_action(status)
    police_next_pos = police_action.dest(police.pos)
    if status.map.wall(police_next_pos):
        return 0
    police.move(police_next_pos)
    status.new_step()
    reward = -status.get_reward(((0, 0), (0, 0)), (police_current_pos, police_next_pos))
    police.q_learning.learn(police_current_pos, police_action, reward, police_next_pos)
    status.police.pos = police_next_pos
    return reward


def execute_r_g(status, thief, police):
    thief.move(thief.get_action(status).dest(thief.pos))
    police.move(police.get_action(status).dest(police.pos))
    status.new_step()


def main():
    over_step = 0
    over_time = 0
    record_q_table = defaultdict(lambda: np.zeros(5))

    for eposide in range(5):
        pg.init()
        pg.display.set_caption("Chase AI")
        cfg = Config()
        cfg.load(Path(__file__).parent.joinpath("config.json"))

        map = create_map("senior")
        thief, police = create_q_r_roles()
        # thief, police = create_r_r_roles()
        # thief, police = create_s_q_roles()
        # thief, police = create_q_g_roles(map)
        # thief, police = create_r_g_roles(map)
        status = Status()
        status.map = map
        status.step = 0
        status.thief = thief
        status.police = police
        start_time = time.time()

        # when use inherit q table
        thief.q_learning.set_q_table(record_q_table)
        iteration = 0

        displayer = Displayer(map, status, cfg.fps)
        # for event in pg.event.get():
        while True:
            iteration = iteration + 1
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
            if not status.game_end():
                # when use q learing
                if iteration == 100:
                    start_time = time.time()
                execute_q(status, thief, police, iteration)

                # execute_r_g(status, thief, police)
                displayer.update()
            else:
                end_time = time.time()
                status.time = end_time - start_time
                print(f"The game ended with {status.step} steps.")
                print(f"The game ended with {status.time} time.")
                break
        # when use inherit q table
        record_q_table = thief.q_learning.q_table
        over_time = over_time + status.time
        over_step = over_step + status.step
    print(f"mean step: {over_step / 5} ")
    print(f"mean time: {over_time / 5} ")


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
