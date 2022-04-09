'''
Author: Guowen Liu
Date: 2022-04-04 23:10:47
LastEditors: Guowen Liu
LastEditTime: 2022-04-09 01:56:24
FilePath: \AI-Group-Project\src\main.py
Description: 

Copyright (c) 2022 by Guowen Liu, All Rights Reserved. 
'''
from hashlib import algorithms_available
import logging
from re import A
import sys
from random import randint, random
from pathlib import Path

import pygame as pg
from pygame.locals import *

from role import RandomFlyRole, AStarPolice, RandomRole, GeneticPolice, StayRole, GeneticThief
from map import Map, Terrain, create_map
from src.qlearning import QLearningPolice, QLearningThief, execute_q
from status import Status
from config import Config
from displayer import Displayer
# import matplotlib.pyplot as plt
import time


def create_roles(police_algorithm, thief_algorithm, map, heuristic, num_iteration=100, mutation_rate=0.3):
    # Police
    if police_algorithm == "A*":
        police = AStarPolice(map, heuristic)
    elif police_algorithm == "genetic_police":
        police = GeneticPolice(map, num_iteration, mutation_rate)
    elif police_algorithm == "qlearning_police":
        police = QLearningPolice(list(range(5)), epsilon=0.1)
    elif police_algorithm == "stay":
        police = StayRole()
    elif police_algorithm == "randome":
        police = RandomRole()

    # Thief
    if thief_algorithm == "genetic_thief":
        thief = GeneticThief(map, num_iteration, mutation_rate)
    elif thief_algorithm == "qlearning_thief":
        thief = QLearningThief(list(range(5)), epsilon=0.01)
    elif thief_algorithm == "stay":
        thief = StayRole()
    elif thief_algorithm == "random":
        thief = RandomRole()

    thief.move((0, 9))
    police.move((24, 0))
    return thief, police


# def create_thief_role(map, num_iteration=100, mutation_rate=0.3):
# thief = RandomRole()
#    thief = GeneticThief(map, num_iteration, mutation_rate)
#    thief.move((0,9))
#    return thief

# def create_police_role(map, num_iteration=100, mutation_rate=0.3):

# police = AStarPolice(map, heuristic)
# police = RandomRole()
#    police = GeneticPolice(map, num_iteration, mutation_rate)
#    police.move((24, 0))
#    return police

def main(map_level, police_algorithm, thief_algorithm):
    num_iteration = 100
    mutation_rate = 0.3
    pg.init()
    pg.display.set_caption("Chase AI")

    cfg = Config()
    cfg.load(Path(__file__).parent.joinpath("config.json"))

    map = create_map(map_level)
    thief, police = create_roles(police_algorithm, thief_algorithm, map, cfg.heuristic, num_iteration, mutation_rate)
    status = Status()
    status.map = map
    status.thief = thief
    status.police = police
    iteration = 0

    displayer = Displayer(map, status, cfg.fps)

    while True:
        iteration = iteration + 1
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
        if not status.game_end():
            if police_algorithm == "qlearning_police":
                execute_q(status, police, thief, iteration)
            elif thief_algorithm == "qlearning_thief":
                execute_q(status, thief, police, iteration)
            else:
                thief.move(thief.get_action(status).dest(thief.pos))
                police.move(police.get_action(status).dest(police.pos))
                status.new_step()
            displayer.update()
        else:
            print(f"The game ended with {status.step} steps.")
            break
    return status.step


def command_line():
    map_all_level = "junior intermediate senior"
    all_police_algorithm = "A* genetic_police qlearning_police random stay"
    all_thief_algorithm = "genetic_thief qlearning_thief random stay"
    map_level, police_algorithm, thief_algorithm = sys.argv[1:4]
    if map_level in map_all_level and police_algorithm in all_police_algorithm and thief_algorithm in all_thief_algorithm:
        main(map_level, police_algorithm, thief_algorithm)
    else:
        print("Wrong Parameters")
    return


def main_for_evaluation():
    average_step = []
    iteration = [5, 25, 50, 100, 250, 500]  # 100
    mutation_rate = [0, 0.1, 0.2, 0.3, 0.5, 0.7]  # 0.3
    map_size = ["junior", "intermediate", "senior"]
    # for iter in iteration:
    # for iter in mutation_rate:
    for size in map_size:
        step_list = []
        time_list = []
        for _ in range(20):
            # step = main(num_iteration=100, mutation_rate=iter)
            step = main(map_size=size)
            step_list.append(step)
        average_step.append(sum(step_list) / len(step_list))
    print(average_step)
    # plt.plot(iteration, average_step, label="Average step")
    # plt.xlabel("Iteration")
    # plt.ylabel("Steps")
    # plt.title("Average step and time for different iteration of genetic algorithm")
    # plt.show()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    try:
        command_line()
        # main()
        # main_for_evaluation()
    except SystemExit:
        pass
    except BaseException as err:
        logger.exception(err)
        sys.exit(1)
