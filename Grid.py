import numpy as np
from copy import deepcopy, copy
from typing import List
import matplotlib.pyplot as plt
from math import exp, sqrt

from Cell import Cell, StalkCell, TipCell, AttractorCell
from Context import GridContext, CellContext, Action, ActionType, Point, ContextRequest
from utils import get_tile_neighborhood, get_tile_radius_outer_ring, DEFAULTS


class Tile:
    def __init__(self, attraction: int = 0, cell: Cell = None) -> None:
        self.attraction = attraction
        self.cell = cell

    def get_attraction(self):
        return self.attraction


class Grid:
    # init_config: : Dict(str, List(Point)) --type hinting
    def __init__(self, width: int, height: int, init_config):
        self.height = height
        self.width = width
        self.grid = [[Tile() for i in range(width)] for j in range(height)]
        self.init_grid_objects(init_config)

    def __getitem__(self, key:Point) -> Tile:
        return self.grid[key.x][key.y]
    def __setitem__(self, key:Point, value: Tile):
        self.grid[key.x][key.y] = value

    def init_grid_objects(self, init_config):
        if 'endothelial_cells' in init_config:
            for ec in init_config['endothelial_cells']:
                self[ec].cell = StalkCell()

        # TODO: REMOVE THIS. WE NEVER START WITH TIP CELLS, THIS IS ONLY FOR TESTING.
        if 'tip_cells' in init_config:
            for tip_cell in init_config['tip_cells']:
                self[tip_cell].cell = TipCell()

        if 'attractor_cells' in init_config:
            for att_cell in init_config['attractor_cells']:  # Tissue / Organ / Tumor
                self[att_cell].cell = AttractorCell()
                self[att_cell].attraction += self[att_cell].cell.attraction_generated
                src_attraction = self[att_cell].attraction

                # get_tile_neighborhood currently doesn't use euclidean distance and might return a few extra tiles (depends on ceil/floor)
                radius = int(np.ceil(np.log(src_attraction * (1/DEFAULTS["attraction"]["update_precision"])) / DEFAULTS["attraction"]["decay_coef"]))
                for point in get_tile_neighborhood(location=att_cell, radius = radius, max_width = self.width, max_height = self.height):
                    self[point].attraction = round(src_attraction * np.exp(-DEFAULTS["attraction"]["decay_coef"] * att_cell.dist(point)),1)
 
            print(self.get_potential_matrix(), '\n')
        self.visualize_potential_matrix()

    def get_potential_matrix(self):
        vec_func = np.vectorize(Tile.get_attraction)
        return vec_func(self.grid)

    def visualize_potential_matrix(self):
        pot_mat = self.get_potential_matrix()
        plt.imshow(pot_mat, cmap='viridis')

    def next_gen(self):
        next_grid = deepcopy(self)
        for x in range(self.height):
            for y in range(self.width):
                cell = self.grid[x][y].cell
                if (cell):
                    cell_context = cell.get_context()
                    actions = cell.get_actions(self.generate_context(
                                               cell_context=cell_context, cell_location=Point(x, y)))
                    next_grid.exec_cell_actions(actions=actions, cell_location=Point(x, y))
        return next_grid

    def generate_context(self, cell_context: CellContext, cell_location: Point):
        grid_context = {}
        attractions = {}

        if (ContextRequest.ATTRACTION_IN_NEIGHBORHOOD in cell_context):
            for neighbor_tile in get_tile_radius_outer_ring(location=cell_location, radius=1, max_width=self.width, max_height=self.height):
                
                attractions[neighbor_tile - cell_location] = self[neighbor_tile].attraction

            grid_context[ContextRequest.ATTRACTION_IN_NEIGHBORHOOD] = attractions

        return grid_context

    def exec_cell_actions(self, actions: List[Action], cell_location: Point):
        for action in actions:
            if action.type == ActionType.MIGRATE and action.dst != Point(0,0):
                self[action.dst + cell_location].cell = self[cell_location].cell
                self[cell_location].cell = None             
                # TODO: remember to update potential if tip moved
                # undo all of the attractions
                # redo

    def to_matrix(self):
        output = np.zeros(shape=(self.height, self.width), dtype=int)
        for x in range(self.height):
            for y in range(self.width):
                grid_cell = self.grid[x][y].cell
                if grid_cell != None:
                    output[x][y] = int(grid_cell.is_alive())
        return output
