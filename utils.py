import json
import numpy as np
from enum import Enum

CONFIG = None
with open("./config.json", "r") as config_file:
    CONFIG = json.load(config_file)

DEFAULTS = CONFIG["defaults"]

        
class GridStatistics():
    def __init__(self, num_cells=0, num_tip=0, num_stalk=0, num_attractor=0, avg_num_neighbors=0):
        self.num_cells = num_cells
        self.num_tip = num_tip
        self.num_stalk = num_stalk
        self.num_attractor = num_attractor
        self.avg_num_neighbors = avg_num_neighbors
    
    def add_tip_cell(self):
        self.num_cells += 1
        self.num_tip += 1
    
    def add_stalk_cell(self):
        self.num_cells += 1
        self.num_stalk += 1
    def add_attractor_cell(self):
        self.num_cells += 1
        self.num_attractor += 1

    def __add__(self, other_stats):
        num_cells = self.num_cells + other_stats.num_cells
        num_tip = self.num_tip + other_stats.num_tips
        num_stalk = self.num_stalk + other_stats.num_stalk
        num_attractor = self.num_attractor + other_stats.num_attractor
        return GridStatistics(num_cells, num_tip, num_stalk, num_attractor)
    
class EngineStatistics():
    def __init__(self, num_generations:int = 0, area:int=1):
        self.num_generations = num_generations
        self.num_cell_history = np.zeros(shape=num_generations)
        self.num_tip_history = np.zeros(shape=num_generations)
        self.num_stalk_history = np.zeros(shape=num_generations)
        self.generations = num_generations
        self.area = area
        self.clustering_coef = -1

    def update(self, gen:int, stats:GridStatistics) ->None: 
        self.num_cell_history[gen] = stats.num_cells
        self.num_tip_history[gen] = stats.num_tip
        self.num_stalk_history[gen] = stats.num_stalk
        return
    
    def update_clustering_coef(self, coef:float) ->None:
        self.clustering_coef = coef
    
    def __str__(self) -> str:
        return f"Number of cells throught generations:\n{self.num_cell_history}\nNumber of TIP cells throught generations:\n{self.num_tip_history}\n \
    Number of STALK cells throught generations:\n{self.num_stalk_history}\n"

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
    def __init__(self, dst : Point, type : ActionType):
        self.dst = dst
        self.type = type

def attraction_to_radius(attraction: float):
    radius = 0
    if (attraction != 0):
        radius = int(np.ceil(np.log(np.abs(attraction) * (1/DEFAULTS["attraction"]["update_precision"])) / DEFAULTS["attraction"]["decay_coef"]))
    return radius

def attraction_decay(src_attraction : float, dist: float):
    attraction = src_attraction * np.exp(-DEFAULTS["attraction"]["decay_coef"] * dist)
    return attraction

def get_tile_neighborhood(location : Point, radius, max_width, max_height, include_self = False):
    pts =  lambda x, y : [Point(x2, y2) for x2 in range(x-radius, x+radius+1)
                            for y2 in range(y-radius, y+radius+1)
                            if (-1 < x < max_width and
                                -1 < y < max_height and
                                ((x != x2 or y != y2) or include_self) and
                                (0 <= x2 < max_width) and
                                (0 <= y2 < max_height))]
    return pts(location.x, location.y)

def get_tile_radius_outer_ring(location : Point, radius, max_width, max_height):
    horizontal =  lambda x, y : [Point(x2, y2) for x2 in (x-radius, x+radius)
                            for y2 in range(y-radius, y+radius+1)
                            if (0 <= x < max_width and
                                0 <= y < max_height and
                                (x != x2 or y != y2) and
                                (0 <= x2 < max_width) and
                                (0 <= y2 < max_height))]
                            
    vertical =  lambda x, y : [Point(x2, y2) for x2 in range(x-radius, x+radius+1)
                        for y2 in (y-radius, y+radius)
                        if (0 <= x < max_width and
                            0 <= y < max_height and
                            (x != x2 or y != y2) and
                            (0 <= x2 < max_width) and
                            (0 <= y2 < max_height))]
    
    return set(horizontal(location.x, location.y) + vertical(location.x, location.y))

