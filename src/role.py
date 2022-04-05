from enum import IntEnum
from random import randint

from search import AStar
from genetic import Genetic

class Action(IntEnum):
    Stay = 0
    Up = 1
    Down = 2
    Left = 3
    Right = 4

    def dest(self, src):
        if self.value == Action.Stay:
            return src
        elif self.value == Action.Up:
            return src[0], src[1] + 1
        elif self.value == Action.Down:
            return src[0], src[1] - 1
        elif self.value == Action.Left:
            return src[0] - 1, src[1]
        elif self.value == Action.Right:
            return src[0] + 1, src[1]
        else:
            assert False

    @staticmethod
    def next(src, dest):
        horizontal_action = Action.Stay
        if src[0] < dest[0]:
            horizontal_action = Action.Right
        elif src[0] > dest[0]:
            horizontal_action = Action.Left

        vertical_action = Action.Stay
        if src[1] < dest[1]:
            vertical_action = Action.Up
        elif src[1] > dest[1]:
            vertical_action = Action.Down
        
        if horizontal_action == Action.Stay:
            return vertical_action
        elif vertical_action == Action.Stay:
            return horizontal_action
        else:
            return [horizontal_action, vertical_action][randint(0, 1)]

class Role:
    def __init__(self):
        self._pos = None
    
    def move(self, pos):
        self._pos = pos

    def get_action(self, status):
        assert False

    @property
    def pos(self):
        return self._pos


class RandomRole(Role):
    def get_action(self, status):
        actions = []
        for action in Action:
            dest = action.dest(self.pos)
            if not status.map.wall(dest):
                actions.append(action)
        return actions[randint(0, len(actions) - 1)]


class RandomFlyRole(Role):
    def get_action(self, status):
        actions = []
        for action in Action:
            dest = action.dest(self.pos)
            if status.map.valid(dest):
                actions.append(action)
        return actions[randint(0, len(actions) - 1)]


class _AStarRole(Role):
    def __init__(self, map, heuristic):
        super().__init__()
        self._heuristic = heuristic
        self._a_star = AStar(map, heuristic)

    def get_action(self, status):
        path = self._a_star.find_path(self._pos, self._target(status).pos)
        return Action.next(self._pos, path[1]) if len(path) > 1 else Action.Stay
    
    def _target(self, status):
        assert False


class AStarEnemy(_AStarRole):
    def _target(self, status):
        return status.agent

class GeneticRole(Role):
    def __init__(self, map):
        super().__init__()
        self._genetic = Genetic(map)

    def get_action(self, status):
        path = self._genetic.find_path(self._pos, self._target(status).pos)
        return Action.next(self._pos, path[1]) if len(path) > 1 else Action.Stay

    def _target(self, status):
        assert False


class GeneticEnemy(GeneticRole):
    def _target(self, status):
        return status.agent