# -*- coding = utf-8 -*-
# @Time : 05/04/2022 10:36
# @Author : Kiser
# @File : genetic.py
# @Software : PyCharm
import random
import math


class Genetic:
    def __init__(self, map) -> None:
        self._map = map  # MAY NEED UPDATE
        self.is_visited = [[0] * self._map.height for _ in range(self._map.width)]
        self.routes = []
        self.actions = []
        self.num_population = 20
        self.num_iteration = 25 # could change, depend on running time

    def clear_visited(self):
        self.is_visited = [[0] * self._map.height for _ in range(self._map.width)]

    def direction_to_route(self, src, dir):
        route = []
        route.append(src)
        prev = src
        for i in range(len(dir)):
            if dir[i] == 1:
                prev = (prev[0], prev[1] - 1)
                route.append(prev)
            elif dir[i] == 2:
                prev = (prev[0], prev[1] + 1)
                route.append(prev)
            elif dir[i] == 3:
                prev = (prev[0] - 1, prev[1])
                route.append(prev)
            elif dir[i] == 4:
                prev = (prev[0] + 1, prev[1])
                route.append(prev)
        return route

    def route_to_direction(self, route):
        # 1,2,3,4: 左右上下
        dir = []
        for i in range(1, len(route)):
            prev = route[i - 1]
            curr = route[i]
            if prev[0] == curr[0] and prev[1] == curr[1] + 1:
                dir.append(1)
            elif prev[0] == curr[0] and prev[1] == curr[1] - 1:
                dir.append(2)
            elif prev[0] == curr[0] + 1 and prev[1] == curr[1]:
                dir.append(3)
            elif prev[0] == curr[0] - 1 and prev[1] == curr[1]:
                dir.append(4)
        return dir

    def generate_random_route(self, src, dest, step, route):
        if src == dest:
            self.routes.append(route)
            print(route)
            return True
        elif step == 10:
            self.routes.append(route)
            print(route)
            return True
        neighbors_ = self._map.neighbors(src)
        random.shuffle(neighbors_)
        for neighbor in neighbors_:
            x = neighbor[0]
            y = neighbor[1]
            if self.is_visited[x][y] == 0:
                self.is_visited[x][y] = 1
                route.append(neighbor)
                if self.generate_random_route(neighbor, dest, step + 1, route):
                    return True
                route = route[:len(route) - 1]
                self.is_visited[x][y] = 0
                return False
        return False

    def fitness_score(self, dest, route):
        # determine how fits an individual is, return a fitness score to each individual
        # The probability that an individual will be selected for reproduction is based on its fitness score
        ans = math.inf
        x = route[len(route) - 1][0] - dest[0]
        y = route[len(route) - 1][1] - dest[1]
        ans = min(len(route) + math.sqrt(math.pow(x, 2) + math.pow(y, 2)), ans)
        return ans
