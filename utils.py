import json
import numpy as np
from enum import Enum

CONFIG = None
with open("./config.json", "r") as config_file:
    CONFIG = json.load(config_file)

DEFAULTS = CONFIG["defaults"]


class ActionType(Enum):
    MIGRATE = 1
    PROLIF = 2
    SPROUT = 3


class ContextRequest(Enum):
    ATTRACTION_IN_NEIGHBORHOOD = 1
    NUM_NEIGHBORS = 2
    NEIGHBORS_NEIGHBORS = 3


class ModifierType(Enum):
    ATTRACTION_MATRIX = 1


class Point():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Point(x, y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def dist(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


class Action():
    def __init__(self, dst: Point, type: ActionType):
        self.dst = dst
        self.type = type


def attraction_to_radius(attraction: float):
    radius = 0
    if (attraction != 0):
        radius = int(np.ceil(np.log(np.abs(
            attraction) * (1/DEFAULTS["attraction"]["update_precision"])) / DEFAULTS["attraction"]["decay_coef"]))
    return radius


def attraction_decay(src_attraction: float, dist: float):
    attraction = src_attraction * \
        np.exp(-DEFAULTS["attraction"]["decay_coef"] * dist)
    return attraction


def get_tile_neighborhood(location: Point, radius, max_width, max_height, include_self=False):
    def pts(x, y): return [Point(x2, y2) for x2 in range(x-radius, x+radius+1)
                           for y2 in range(y-radius, y+radius+1)
                           if (-1 < x < max_width and
                               -1 < y < max_height and
                               ((x != x2 or y != y2) or include_self) and
                               (0 <= x2 < max_width) and
                               (0 <= y2 < max_height))]
    return pts(location.x, location.y)


def get_tile_radius_outer_ring(location: Point, radius, max_width, max_height):
    def horizontal(x, y): return [Point(x2, y2) for x2 in (x-radius, x+radius)
                                  for y2 in range(y-radius, y+radius+1)
                                  if (0 <= x < max_width and
                                      0 <= y < max_height and
                                      (x != x2 or y != y2) and
                                      (0 <= x2 < max_width) and
                                      (0 <= y2 < max_height))]

    def vertical(x, y): return [Point(x2, y2) for x2 in range(x-radius, x+radius+1)
                                for y2 in (y-radius, y+radius)
                                if (0 <= x < max_width and
                                    0 <= y < max_height and
                                    (x != x2 or y != y2) and
                                    (0 <= x2 < max_width) and
                                    (0 <= y2 < max_height))]

    return set(horizontal(location.x, location.y) + vertical(location.x, location.y))
