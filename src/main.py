'''
Author: Guowen Liu
Date: 2022-04-04 23:10:47
LastEditors: Guowen Liu
LastEditTime: 2022-04-01 23:22:59
FilePath: \AI-Group-Project\src\main.py
Description: 

Copyright (c) 2022 by Guowen Liu, All Rights Reserved. 
'''
import logging
from re import A
import sys
from random import randint
from pathlib import Path

import pygame as pg
from pygame.locals import *

from role import RandomFlyRole, AStarPolice, RandomRole, GeneticPolice, StayRole, GeneticThief
from map import Map, Terrain
from status import Status
from config import Config
from displayer import Displayer
#import matplotlib.pyplot as plt
import time


def create_map():
    spots = [[Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Wall,Terrain.Plain, Terrain.Wall, Terrain.Wall, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Wall, Terrain.Wall, Terrain.Wall, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Wall],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Wall, Terrain.Wall, Terrain.Plain, Terrain.Wall],
             [Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Plain],
             [Terrain.Wall, Terrain.Wall, Terrain.Wall, Terrain.Wall, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Wall, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Wall, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Wall, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Wall, Terrain.Wall, Terrain.Plain, Terrain.Plain],
             [Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Wall, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Wall],
             [Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Wall, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Wall]]
    return Map(spots)


def create_roles(map, heuristic, num_iteration=100, mutation_rate=0.3):
    # thief = RandomRole()
    thief = GeneticThief(map, num_iteration, mutation_rate=0.7)
    thief.move((0,9))
    # police = AStarPolice(map, heuristic)
    #police = RandomRole()
    police = GeneticPolice(map, num_iteration, mutation_rate)
    police.move((24, 0))
    return thief, police

#def create_thief_role(map, num_iteration=100, mutation_rate=0.3):
    # thief = RandomRole()
#    thief = GeneticThief(map, num_iteration, mutation_rate)
#    thief.move((0,9))
#    return thief

#def create_police_role(map, num_iteration=100, mutation_rate=0.3):

    # police = AStarPolice(map, heuristic)
    #police = RandomRole()
#    police = GeneticPolice(map, num_iteration, mutation_rate)
#    police.move((24, 0))
#    return police

def main():
    pg.init()
    pg.display.set_caption("Chase AI")

    cfg = Config()
    cfg.load(Path(__file__).parent.joinpath("config.json"))

    map = create_map()
    thief, police = create_roles(map, cfg.heuristic)
    status = Status()
    status.map = map
    status.thief = thief
    status.police = police

    displayer = Displayer(map, status, cfg.fps)

    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
        if not status.game_end():
            thief.move(thief.get_action(status).dest(thief.pos))
            police.move(police.get_action(status).dest(police.pos))
            status.new_step()
            displayer.update()
        else:
            print(f"The game ended with {status.step} steps.")
            break

def main_for_plot():
    average_step = []
    average_time = []
    iteration = [5, 25, 50, 100, 250, 500] #100
    mutation_rate = [0, 0.1, 0.2, 0.3, 0.5, 0.7] #0.3
    iter = 0
    #for iter in range(len(iteration)):
    for iter in range(len(mutation_rate)):
        step_list = []
        time_list = []
        for i in range(5):
            start = time.perf_counter()
            pg.init()
            pg.display.set_caption("Chase AI")

            cfg = Config()
            cfg.load(Path(__file__).parent.joinpath("config.json"))

            map = create_map()
            thief, police = create_roles(map, cfg.heuristic, num_iteration=100, mutation_rate=mutation_rate[iter])
            #thief, police = create_roles(map, cfg.heuristic, num_iteration=iteration[iter], mutation_rate=0.3)
            #thief = create_thief_role(map, num_iteration=100, mutation_rate=mutation_rate[iter])
            #police = create_police_role(map, num_iteration=100, mutation_rate=0.3)
            status = Status()
            status.map = map
            status.thief = thief
            status.police = police

            displayer = Displayer(map, status, cfg.fps)

            while True:
                for event in pg.event.get():
                    if event.type == QUIT:
                        pg.quit()
                        sys.exit()
                if not status.game_end():
                    thief.move(thief.get_action(status).dest(thief.pos))
                    police.move(police.get_action(status).dest(police.pos))
                    status.new_step()
                    displayer.update()
                else:
                    print(f"The game ended with {status.step} steps.")
                    break
            end = time.perf_counter()
            step_list.append(status.step)
            time_list.append(end - start)
        average_step.append(sum(step_list)/len(step_list))
        average_time.append(sum(time_list)/len(time_list))
    print(average_step)
    print(average_time)
    #plt.plot(iteration, average_step, label="Average step")
    #plt.plot(iteration, average_time, label="Average time")
    #plt.xlabel("Iteration")
    #plt.ylabel("Steps/time(seconds)")
    #plt.title("Average step and time for different iteration of genetic algorithm")
    #plt.show()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    try:
        main()
        #main_for_plot()
    except SystemExit:
        pass
    except BaseException as err:
        logger.exception(err)
        sys.exit(1)