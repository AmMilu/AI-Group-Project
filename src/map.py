from enum import Enum, auto
import math


def create_map(size):
    spots_junior = [[Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
              Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
              Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
              Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
              Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
              Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
              Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
              Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
              Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
              Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
              Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
              Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
              Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
              Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
              Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
              Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
              Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
              Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
              Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
              Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
              Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
              Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
              Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
              Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
              Terrain.Plain, Terrain.Plain, Terrain.Plain],
             [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
              Terrain.Plain, Terrain.Plain, Terrain.Plain]]
    spots_intermediate = [
        [Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall,
         Terrain.Plain, Terrain.Wall, Terrain.Plain],
        [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
         Terrain.Plain, Terrain.Plain, Terrain.Plain],
        [Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain,
         Terrain.Wall, Terrain.Plain, Terrain.Wall],
        [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
         Terrain.Plain, Terrain.Plain, Terrain.Plain],
        [Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall,
         Terrain.Plain, Terrain.Wall, Terrain.Plain],
        [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
         Terrain.Plain, Terrain.Plain, Terrain.Plain],
        [Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain,
         Terrain.Wall, Terrain.Plain, Terrain.Wall],
        [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
         Terrain.Plain, Terrain.Plain, Terrain.Plain],
        [Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall,
         Terrain.Plain, Terrain.Wall, Terrain.Plain],
        [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
         Terrain.Plain, Terrain.Plain, Terrain.Plain],
        [Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain,
         Terrain.Wall, Terrain.Plain, Terrain.Wall],
        [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
         Terrain.Plain, Terrain.Plain, Terrain.Plain],
        [Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall,
         Terrain.Plain, Terrain.Wall, Terrain.Plain],
        [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
         Terrain.Plain, Terrain.Plain, Terrain.Plain],
        [Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain,
         Terrain.Wall, Terrain.Plain, Terrain.Wall],
        [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
         Terrain.Plain, Terrain.Plain, Terrain.Plain],
        [Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall,
         Terrain.Plain, Terrain.Wall, Terrain.Plain],
        [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
         Terrain.Plain, Terrain.Plain, Terrain.Plain],
        [Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain,
         Terrain.Wall, Terrain.Plain, Terrain.Wall],
        [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
         Terrain.Plain, Terrain.Plain, Terrain.Plain],
        [Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall,
         Terrain.Plain, Terrain.Wall, Terrain.Plain],
        [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
         Terrain.Plain, Terrain.Plain, Terrain.Plain],
        [Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain,
         Terrain.Wall, Terrain.Plain, Terrain.Wall],
        [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
         Terrain.Plain, Terrain.Plain, Terrain.Plain],
        [Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall,
         Terrain.Plain, Terrain.Wall, Terrain.Plain]]
    spots_senior = [
        [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
         Terrain.Plain, Terrain.Plain, Terrain.Plain],
        [Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain,
         Terrain.Plain, Terrain.Plain, Terrain.Plain],
        [Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Plain,
         Terrain.Plain, Terrain.Wall, Terrain.Plain],
        [Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
         Terrain.Plain, Terrain.Plain, Terrain.Plain],
        [Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Wall, Terrain.Wall,
         Terrain.Wall, Terrain.Wall, Terrain.Plain],
        [Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
         Terrain.Plain, Terrain.Plain, Terrain.Plain],
        [Terrain.Plain, Terrain.Wall, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Wall,
         Terrain.Plain, Terrain.Wall, Terrain.Wall],
        [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Plain,
         Terrain.Plain, Terrain.Plain, Terrain.Wall],
        [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Wall, Terrain.Wall, Terrain.Plain,
         Terrain.Plain, Terrain.Wall, Terrain.Wall],
        [Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
         Terrain.Plain, Terrain.Plain, Terrain.Plain],
        [Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
         Terrain.Plain, Terrain.Plain, Terrain.Plain],
        [Terrain.Wall, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
         Terrain.Plain, Terrain.Wall, Terrain.Plain],
        [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Plain,
         Terrain.Plain, Terrain.Wall, Terrain.Plain],
        [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Wall,
         Terrain.Plain, Terrain.Wall, Terrain.Plain],
        [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Plain,
         Terrain.Plain, Terrain.Plain, Terrain.Plain],
        [Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
         Terrain.Wall, Terrain.Plain, Terrain.Wall],
        [Terrain.Plain, Terrain.Wall, Terrain.Wall, Terrain.Wall, Terrain.Wall, Terrain.Plain, Terrain.Plain,
         Terrain.Wall, Terrain.Plain, Terrain.Wall],
        [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
         Terrain.Plain, Terrain.Plain, Terrain.Plain],
        [Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Plain,
         Terrain.Plain, Terrain.Plain, Terrain.Plain],
        [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Wall, Terrain.Wall, Terrain.Wall, Terrain.Plain,
         Terrain.Wall, Terrain.Wall, Terrain.Plain],
        [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
         Terrain.Plain, Terrain.Plain, Terrain.Plain],
        [Terrain.Wall, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Wall,
         Terrain.Wall, Terrain.Plain, Terrain.Plain],
        [Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
         Terrain.Wall, Terrain.Plain, Terrain.Plain],
        [Terrain.Plain, Terrain.Wall, Terrain.Plain, Terrain.Wall, Terrain.Wall, Terrain.Wall, Terrain.Plain,
         Terrain.Plain, Terrain.Wall, Terrain.Wall],
        [Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain, Terrain.Plain,
         Terrain.Plain, Terrain.Plain, Terrain.Plain]]
    if size == "junior":
        return Map(spots_junior)
    elif size == "intermediate":
        return Map(spots_intermediate)
    elif size == "senior":
        return Map(spots_senior)
    else:
        return Map(spots_junior)


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
