from collections import namedtuple
from enum import Enum

class ActionType(Enum):
    MIGRATE = 1
    DIVIDE = 2
class ContextRequest(Enum):
    ATTRACTION_IN_NEIGHBORHOOD = 1
    

Point = namedtuple('Point', 'x y')

#* Grid gives cell context, cell returns to grid the actions it wants to make
class GridContext():
    def __init__(self, alive_neighbors: int, dead_neighbors: int):
        self.alive_neighbors = alive_neighbors
        self.dead_neighbors = dead_neighbors
class CellContext():
    def __init__(self, radius_alive_neighbors: int, radius_dead_neighbors: int):
        self.radius_alive_neighbors = radius_alive_neighbors
        self.radius_dead_neighbors = radius_dead_neighbors
        
class Action():
    def __init__(self, dst : Point, type : ActionType):
        self.dst = dst
        self.type = type