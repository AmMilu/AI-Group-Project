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
import sys
from random import randint
from pathlib import Path

import pygame as pg
from pygame.locals import *

from role import RandomFlyRole, AStarPolice, RandomRole, GeneticPolice, StayRole
from map import Map, Terrain
from status import Status
from config import Config
from displayer import Displayer


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


def create_roles(map, heuristic):
    thief = RandomRole()
    thief.move((0, 9))
    #police = AStarPolice(map, heuristic)
    #police = RandomRole()
    police = GeneticPolice(map)
    police.move((24, 0))
    return thief, police


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
