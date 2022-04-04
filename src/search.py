class AStar:
    def __init__(self, map, heuristic):
        self._heuristic = heuristic
        self._map = map
        self._spots = [[None] * map.height for _ in range(map.width)]
        for x in range(map.width):
            for y in range(map.height):
                self._spots[x][y] = _Spot((x, y))

    def find_path(self, src, dest):
        """
        Find a path to the opponent.
        """
        self._clear_spots()
        open_spots, close_spots = [], []

        def min_spot():
            spot = min(open_spots, key=lambda spot: spot.f)
            open_spots.remove(spot)
            return spot

        open_spots.append(self._spots[src[0]][src[1]])
        while open_spots:
            spot = min_spot()
            if spot.pos == dest:
                return spot.retrace()
            close_spots.append(spot)

            for neighbor in self._map.neighbors(spot.pos):
                neighbor_spot = self._spots[neighbor[0]][neighbor[1]]
                if neighbor_spot in close_spots:
                    continue
                new_g = spot.g + self._heuristic(spot.pos, neighbor)
                new_path = False
                if neighbor_spot in open_spots:
                    if new_g < neighbor_spot.g:
                        neighbor_spot.g = new_g
                        new_path = True
                else:
                    neighbor_spot.g = new_g
                    new_path = True
                    open_spots.append(neighbor_spot)

                if new_path:
                    neighbor_spot.g = new_g
                    neighbor_spot.prev = spot
        return []

    def _clear_spots(self):
        """
        Clear the pathfinding record.
        """
        for x in range(len(self._spots)):
            for y in range(len(self._spots[0])):
                self._spots[x][y].clear()


class _Spot:
    def __init__(self, pos):
        self._pos = pos
        self.prev = None
        self.g = 0
        self.h = 0

    @property
    def pos(self):
        return self._pos

    @property
    def x(self) -> int:
        return self._pos[0]

    @property
    def y(self) -> int:
        return self._pos[1]

    @property
    def f(self):
        return self.g + self.h

    def retrace(self):
        path = [self.pos]
        spot = self
        while spot.prev:
            path.insert(0, spot.prev.pos)
            spot = spot.prev
        return path

    def clear(self):
        self.prev = None
        self.g = 0
        self.h = 0