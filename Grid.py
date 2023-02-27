import numpy as np
from copy import deepcopy, copy
from typing import List
import matplotlib.pyplot as plt
from math import exp, sqrt
from Cell import Cell, StalkCell, TipCell, AttractorCell
from utils import GridStatistics, get_tile_neighborhood, get_tile_radius_outer_ring, DEFAULTS, attraction_to_radius, attraction_decay, \
    Action, ActionType, Point, ContextRequest, ModifierType

class Tile:
    def __init__(self, attraction: int = 0, cell: Cell = None) -> None:
        self.attraction = attraction
        self.cell = cell

    def get_attraction(self):
        return self.attraction


class Grid:
    def __init__(self, width: int, height: int, init_config):
        self.height = height
        self.width = width
        self.grid = [[Tile() for i in range(width)] for j in range(height)]
        self.stats = GridStatistics()
        self.init_grid_objects(init_config)

    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height
    
    def get_stats(self) ->GridStatistics:
        return self.stats
    
    def get_area(self):
        return self.width*self.height

    def __getitem__(self, key:Point) -> Tile:
        return self.grid[key.x][key.y]
    def __setitem__(self, key:Point, value: Tile):
        self.grid[key.x][key.y] = value

    def init_grid_objects(self, init_config):
        if 'stalk_cells' in init_config:
            for stalk_cell in init_config['stalk_cells']:
                self[stalk_cell].cell = StalkCell()
                self.apply_modifier(type=ModifierType.ATTRACTION_MATRIX, cell_location=stalk_cell, neg_effect=False)
                self.stats.add_stalk_cell()

        # TODO: REMOVE THIS. WE NEVER START WITH TIP CELLS, THIS IS ONLY FOR TESTING.
        if 'tip_cells' in init_config:
            for i, tip_cell in enumerate(init_config['tip_cells']):
                self[tip_cell].cell = TipCell(id=i)
                self.apply_modifier(type=ModifierType.ATTRACTION_MATRIX, cell_location=tip_cell, neg_effect=False)
                self.stats.add_tip_cell()

        if 'attractor_cells' in init_config:
            for att_cell in init_config['attractor_cells']:  # Tissue / Organ / Tumor
                self[att_cell].cell = AttractorCell()
                self.apply_modifier(type=ModifierType.ATTRACTION_MATRIX, cell_location=att_cell, neg_effect=False)
                self.stats.add_attractor_cell()

            # print(self.get_potential_matrix(), '\n')
        self.visualize_potential_matrix()

    def apply_modifier(self, type: ModifierType, cell_location: Point, neg_effect: bool = False):
        if (type == ModifierType.ATTRACTION_MATRIX):
            attraction_matrix = self[cell_location].cell.get_modifiers()[ModifierType.ATTRACTION_MATRIX]
            if (neg_effect):
                attraction_matrix = -attraction_matrix
            radius = int(((attraction_matrix.shape[0]-1)/2))
            att_matrix_center = Point(radius, radius)
            for point in get_tile_neighborhood(location=cell_location, radius=radius , max_height=self.height, max_width=self.width, include_self=True):
                matrix_point = att_matrix_center + (point - cell_location)
                self[point].attraction += attraction_matrix[matrix_point.x][matrix_point.y]
        
    def get_potential_matrix(self):
        vec_func = np.vectorize(Tile.get_attraction)
        return vec_func(self.grid)

    def visualize_potential_matrix(self):
        pot_mat = self.get_potential_matrix()
        plt.imshow(pot_mat, cmap='viridis', vmin=0, vmax=1800)

    def next_gen(self):
        actions = {}
        for x in range(self.height):
            for y in range(self.width):
                if (self.grid[x][y].cell):
                    cell_context = self.grid[x][y].cell.get_context()
                    actions[Point(x,y)] = self.grid[x][y].cell.get_actions(self.generate_context(
                                               cell_context=cell_context, cell_location=Point(x, y)))
            
        #! We first iterate over the original board to calculate all necessary changes \
        # and update cell members. Then we copy the grid with updated members to new grid, and then act on it.    
        next_grid = deepcopy(self)
        for tile_actioned in actions:    
            next_grid.exec_cell_actions(actions=actions[tile_actioned], cell_location=tile_actioned)
        return next_grid

    def generate_context(self, cell_context, cell_location: Point):
        grid_context = {}
        attractions = {}
        neighbors_neighbors = {}
        if (ContextRequest.ATTRACTION_IN_NEIGHBORHOOD in cell_context):
            for neighbor_tile in get_tile_radius_outer_ring(location=cell_location, radius=1, max_width=self.width, max_height=self.height):
                attractions[neighbor_tile - cell_location] = self[neighbor_tile].attraction
            grid_context[ContextRequest.ATTRACTION_IN_NEIGHBORHOOD] = attractions

        if (ContextRequest.NUM_NEIGHBORS in cell_context):
            grid_context[ContextRequest.NUM_NEIGHBORS] = self.num_neighbors(cell_location)

        if (ContextRequest.NEIGHBORS_NEIGHBORS in cell_context):
            for neighbor_tile in get_tile_radius_outer_ring(location=cell_location, radius=1, max_width=self.width, max_height=self.height):
                neighbors_neighbors[neighbor_tile - cell_location] = self.num_neighbors(neighbor_tile)
            grid_context[ContextRequest.NEIGHBORS_NEIGHBORS] = neighbors_neighbors


        return grid_context

    def exec_cell_actions(self, actions: List[Action], cell_location: Point):
        for action in actions:
            if action.type == ActionType.MIGRATE:
                
                self.apply_modifier(type = ModifierType.ATTRACTION_MATRIX, cell_location=cell_location, neg_effect= True)
                if(not self[action.dst + cell_location].cell):
                    self[action.dst + cell_location].cell = self[cell_location].cell
                    self.apply_modifier(type = ModifierType.ATTRACTION_MATRIX, cell_location=(action.dst + cell_location), neg_effect= False)
                
                self[cell_location].cell = StalkCell()
                self.stats.add_stalk_cell()
                

            if action.type == ActionType.PROLIF:
                if(not self[action.dst + cell_location].cell):
                    self[action.dst + cell_location].cell = StalkCell()
                    self.apply_modifier(type = ModifierType.ATTRACTION_MATRIX, cell_location=(action.dst + cell_location), neg_effect= False)
                    self.stats.add_stalk_cell()

            
            if action.type == ActionType.SPROUT:
                if(not self[action.dst + cell_location].cell):
                    self[action.dst + cell_location].cell = TipCell(1)
                    self.stats.add_tip_cell()
            



    def to_matrix(self):
        # np.full((width, height), 7)
        output = np.full(shape=(self.height, self.width), fill_value=0, dtype=float)
        for x in range(self.height):
            for y in range(self.width):
                # output[x][y] = 7
                grid_cell = self.grid[x][y].cell
                if type(grid_cell) == StalkCell:
                    output[x][y] = 1
                if type(grid_cell) == TipCell:
                    output[x][y] = 2
                if type(grid_cell) == AttractorCell:
                    output[x][y] = 3
                
                    

        return output

    def num_neighbors(self, location : Point) -> int:
        num = 0
        for neighbor in get_tile_radius_outer_ring(location=location, radius=1, max_width=self.width, max_height=self.height):
            num += int(self[neighbor].cell != None)

        return num
