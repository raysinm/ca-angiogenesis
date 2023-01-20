from enum import Enum

class ActionType(Enum):
    MIGRATE = 1
    DIVIDE = 2
class ContextRequest(Enum):
    ATTRACTION_IN_NEIGHBORHOOD = 1
    

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