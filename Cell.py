from collections import namedtuple
from enum import Enum
from random import uniform, choices
from Context import GridContext, CellContext, Action, ActionType, ContextRequest, Point
from utils import CONFIG


class CellStatus(Enum):
    DEAD = 0
    ALIVE = 1



class Cell:
    def __init__(self, p_migrate=0, attraction_generated=0):
        self.status = CellStatus.ALIVE
        self.attraction_generated = attraction_generated
        self.p_migrate = p_migrate

    def get_actions(self, grid_context: GridContext):
        return []

    def get_context(self) -> CellContext:
        return []

    def is_alive(self):
        return self.status == CellStatus.ALIVE

    def choose_direction(self, grid_context) -> Point:
        direction = Point(0,0) # Default is no movement
        
        attractions = grid_context[ContextRequest.ATTRACTION_IN_NEIGHBORHOOD]
        print(attractions, '\n')
        attraction_sum = sum(attractions.values())
        if(attraction_sum): # If there is attraction
            direction = choices(list(attractions.keys()), [val/attraction_sum for val in attractions.values()])[0]
        return direction


class TipCell(Cell):
    def __init__(self, p_migrate=CONFIG["defaults"]["tip_cell"]["p_migrate"], attraction_generated=CONFIG["defaults"]["tip_cell"]["attraction_generated"]):
        Cell.__init__(self, p_migrate, attraction_generated)

    def get_actions(self, grid_context: GridContext):
        actions = []
        # Migrate
        if (self.should_migrate()):
            actions.append(Action(dst=self.choose_direction(grid_context), type=ActionType.MIGRATE))
        
        return actions

    def get_context(self):
        return [ContextRequest.ATTRACTION_IN_NEIGHBORHOOD]

    def should_migrate(self):
        return uniform(0, 1) < self.p_migrate


class StalkCell(Cell):
    pass


class AttractorCell(Cell):
    def __init__(self, p_migrate=CONFIG["defaults"]["attractor_cell"]["p_migrate"], attraction_generated=CONFIG["defaults"]["attractor_cell"]["attraction_generated"]):
        Cell.__init__(self, p_migrate, attraction_generated)