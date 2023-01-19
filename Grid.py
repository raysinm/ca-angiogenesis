import numpy as np
from copy import deepcopy
from collections import namedtuple
from typing import List


from Cell import Cell, StalkCell,TipCell,AttractorCell
from Context import GridContext, CellContext, Action, ActionType

Point = namedtuple('Point', 'x y')

class Tile:
    def __init__(self, attraction : int = 0, cell : Cell = None) -> None:
        self.attraction = attraction
        self.cell = cell

class Grid: 
    def __init__(self, width: int, height: int, init_config):   #init_config: : Dict(str, List(Point)) --type hinting
        self.height = height
        self.width = width
        self.grid = [[Tile() for i in range(width)] for j in range(height)]
        self.init_grid_objects(init_config)

    def init_grid_objects(self, init_config):
        if 'endothelial_cells' in init_config:
            for c in init_config['endothelial_cells']:
                self.grid[c.x][c.y].cell = StalkCell() 
        
        if 'attractor_cells' in init_config:
            for c in init_config['attractor_cells']: # Tissue / Organ / Tumor
                self.grid[c.x][c.y].cell = AttractorCell()

        # .. More classes of cells supported T.B.D

    def next_gen(self):
        next_grid = deepcopy(self)
        for x in range(self.height):
            for y in range(self.width):
                cell = self.grid[x][y].cell
                if (cell):
                    cell_context = cell.get_context()
                    actions = cell.get_actions(self.generate_context(cell_context=cell_context, point=(x,y)))
                    next_grid.exec_cell_actions(actions=actions, point=(x,y))
        return next_grid
            
    def generate_context(self, cell_context : CellContext, point: Point):
        pass

    def exec_cell_actions(self, actions : List[Action], point: Point):
        # TODO: 1. Implement and test get_context get_actions and generate_context and exec_actions functions. 2. Implement cell die()
        #TODO: add enum for CellStatus.ALIVE, DEAD
        for action in actions:
            if action.type == ActionType.KILL:
                self.grid[action.dst].die()     #* For example, TBD

    def to_matrix(self):
        output = np.zeros(shape=(self.height,self.width), dtype=int)
        for x in range(self.height):
            for y in range(self.width):
                gridcell = self.grid[x][y].cell
                if gridcell != None:
                    output[x][y] = int(gridcell.is_alive())
        return output