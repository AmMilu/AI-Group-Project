from pathlib import Path

import pygame as pg


class Displayer:
    _SPOT_WIDTH = 50
    _SPOT_HEIGHT = 50
    _BACKGROUND_COLOR = (0, 0, 0)

    def __init__(self, map, status, fps):
        self._map = map
        self._status = status
        self._width = map.width * self._SPOT_WIDTH
        self._height = map.height * self._SPOT_HEIGHT
        self._window = pg.display.set_mode((self._width, self._height))
        self._fps_clock = pg.time.Clock()

        res_path = Path(__file__).parent.joinpath("res")
        self._images = {
            "thief": pg.image.load(str(res_path.joinpath("thief.png"))),
            "police": pg.image.load(str(res_path.joinpath("police.png"))),
            "plain": pg.image.load(str(res_path.joinpath("plain.png"))),
            "wall": pg.image.load(str(res_path.joinpath("wall.png"))),
        }

        self._ground_images = [[None] * map.height for _ in range(map.width)]
        self._fps = fps
        for x in range(map.width):
            for y in range(map.height):
                self._ground_images[x][y] = self._images["wall"] if map.wall((x, y)) else self._images["plain"]

    def update(self):
        self._window.fill(self._BACKGROUND_COLOR)
        self._draw_map()
        pg.display.update()
        self._fps_clock.tick(self._fps)

    def _draw_map(self):
        map_surf = pg.Surface((self._width, self._height))
        map_surf.fill(self._BACKGROUND_COLOR)
        for x in range(self._map.width):
            for y in range(self._map.height):
                rect = pg.Rect((x * self._SPOT_WIDTH, y * self._SPOT_HEIGHT,
                                self._SPOT_WIDTH, self._SPOT_HEIGHT))
                map_surf.blit(self._ground_images[x][y], rect)
                if self._status.thief.pos == (x, y):
                    map_surf.blit(self._images["thief"], rect)
                if self._status.police.pos == (x, y):
                    map_surf.blit(self._images["police"], rect)
        self._window.blit(map_surf, map_surf.get_rect())