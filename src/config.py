import json

class Config:
    def __init__(self):
        self._cfg = {}

    @property
    def fps(self):
        return self._cfg["fps"]

    @property
    def heuristic(self):
        def dist(src: tuple[int, int], dest: tuple[int, int]) -> float:
            return abs(src[0] - dest[0]) + abs(src[1] - dest[1])
        return dist

    def load(self, path) -> None:
        with path.open(encoding="utf-8") as file:
            self._cfg = json.load(file)
