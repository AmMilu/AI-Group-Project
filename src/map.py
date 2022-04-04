from enum import Enum, auto
import math


class Terrain(Enum):
    Wall = auto()
    Plain = auto()

    @property
    def cost(self):
        name = self.name.lower()
        if name == "plain":
            return 1
        else:
            return math.inf


class Map:
    def __init__(self, spots):
        self._spots = spots

    @property
    def spots(self):
        return self._spots

    @property
    def width(self):
        return len(self._spots)

    @property
    def height(self):
        return len(self._spots[0])

    def wall(self, pos):
        if not self.valid(pos):
            return True
        else:
            x, y = pos
            return self._spots[x][y] == Terrain.Wall
    
    def valid(self, pos):
        x, y = pos
        if x < 0 or x >= self.width:
            return False
        elif y < 0 or y >= self.height:
            return False
        else:
            return True

    def cost(self, pos):
        if self.wall(pos):
            return Terrain.Wall.cost
        else:
            x, y = pos
            return self._spots[x][y].cost

    def neighbors(self, pos):
        if self.wall(pos):
            return []
        x, y = pos
        spots = []
        if not self.wall((x + 1, y)):
            spots.append((x + 1, y))
        if not self.wall((x - 1, y)):
            spots.append((x - 1, y))
        if not self.wall((x, y + 1)):
            spots.append((x, y + 1))
        if not self.wall((x, y - 1)):
            spots.append((x, y - 1))
        return spots
