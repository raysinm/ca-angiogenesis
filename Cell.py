from collections import namedtuple
from enum import Enum
from Context import GridContext, CellContext, Action

class CellStatus(Enum):
    DEAD = 0
    ALIVE = 1

class Cell:
    def __init__(self):
        self.status = CellStatus.ALIVE
        # self.p_propagate = 0.5
        # self.p_die = 0.5
        # self.cycle = 1
        # self.x, self.y = (x,y)
        # self.max_cycle = max_cycle
    
    # def next(self):
    #     if self.status != CellStatus.ALIVE: return (self.x, self.y)
    #     self.update_probs()
    #     if self.should_die():
    #         return self.die()

    #     self.cycle += 1
    #     self.update_p()

    #     if self.should_propagate():
    #         return self.propagate()
    #     else:
    #         return (self.x, self.y) #Not right
            
    # def update_probs(self):
    #     '''Update probabilities of this cell to divide or to die'''
    #     if self.status == CellStatus.ALIVE:
    #         if self.cycle >= self.max_cycle:
    #             self.p_die = 1.0      

    def get_actions(self, grid_context: GridContext):
        return []

    def get_context(self) -> CellContext:
        pass

    def is_alive(self):
        return self.status == CellStatus.ALIVE

class StalkCell(Cell):
    pass


class AttractorCell(Cell):
    pass

class TipCell(Cell):
    pass