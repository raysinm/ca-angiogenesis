import numpy as np
from copy import deepcopy
from typing import List
import matplotlib.pyplot as plt

from Cell import Cell, StalkCell, TipCell, AttractorCell
from utils import GridStatistics, get_tile_neighborhood, get_tile_radius_outer_ring, Action, ActionType, Point, ContextRequest, ModifierType, CONFIG


class Tile:
    """A class used to represent a single tile in the board:
       each (x,y) index is represented by a tile.
    """

    def __init__(self, attraction: int = 0, cell: Cell = None) -> None:
        """ 

        Args:
            attraction (int, optional): How strongly does this tile attracts cells. Defaults to 0.
            cell (Cell, optional): The biological cell (if exists) in this tile (tip/stalk). Defaults to None.
        """
        self.attraction = attraction
        self.cell = cell

    def get_attraction(self):
        return self.attraction


class Grid:
    """The board of the simulation, a 2 dimensional array of tiles.
    """

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

    def get_stats(self) -> GridStatistics:
        return self.stats

    def get_area(self):
        return self.width*self.height

    def calc_clustering_coef(self) -> float:
        coef = 0
        MAX_NUM_NEIGHBORS = 8
        total_cell_num = self.stats.num_cells
        for y in range(self.width):
            for x in range(self.height):
                if self[Point(x, y)].cell != None:
                    num_neighbors = self.num_neighbors(location=Point(x, y))
                    coef += (num_neighbors/MAX_NUM_NEIGHBORS) * \
                        (1/total_cell_num)
        return coef

    # Implemented index ([]) operator
    def __getitem__(self, key: Point) -> Tile:
        return self.grid[key.x][key.y]

    def __setitem__(self, key: Point, value: Tile):
        self.grid[key.x][key.y] = value

    def init_grid_objects(self, init_config, visualize_potential=False):
        """Initialize the board, placing cells in the tiles and settings the attraction accordingly.
           This function is usually called when creating the first grid. 
           other grids are created by copying the previous one.

        Args:
            init_config (dict): a dictionary containing three keys: stalk_cells, tip_cells, attractor_cells. 
                                each key contains a list of indexes which contain this type of cells.
        """
        if 'stalk_cells' in init_config:
            for stalk_cell in init_config['stalk_cells']:
                self[stalk_cell].cell = StalkCell()
                self.stats.add_stalk_cell()

        if 'tip_cells' in init_config:
            for tip_cell in init_config['tip_cells']:
                self[tip_cell].cell = TipCell()
                self.stats.add_tip_cell()

        if 'attractor_cells' in init_config:
            for att_cell in init_config['attractor_cells']:
                self[att_cell].cell = AttractorCell()
                self.apply_modifier(
                    type=ModifierType.ATTRACTION_MATRIX, cell_location=att_cell)
                self.stats.add_attractor_cell()

        if visualize_potential:
            self.visualize_potential_matrix()

    def apply_modifier(self, type: ModifierType, cell_location: Point, neg_effect: bool = False):
        """Apply a modification to the board. Can support multiple modifier types.
           e.g. If a new attractor cell is created, we need to change the attraction of cells in its area.

        Args:
            type (ModifierType): The modification type.
            cell_location (Point): The location of the modification.
            neg_effect (bool, optional): option used to reverse the modification. Defaults to False.
        """
        # Modify attraction
        if type == ModifierType.ATTRACTION_MATRIX:

            # Get the attraction matrix, a matrix with values of attraction which should be added
            # to tiles in the neighborhood of the attracting cell
            attraction_matrix = self[cell_location].cell.get_modifiers()[
                ModifierType.ATTRACTION_MATRIX]
            if (neg_effect):
                attraction_matrix = -attraction_matrix

            # The neighborhood size to update should match the attraction matrix size.
            radius = int(((attraction_matrix.shape[0]-1)/2))
            att_matrix_center = Point(radius, radius)
            for point in get_tile_neighborhood(location=cell_location, radius=radius, max_height=self.height, max_width=self.width, include_self=True):
                # Convert from attraction matrix to actual board location.
                matrix_point = att_matrix_center + (point - cell_location)
                # Modify attraction.
                self[point].attraction += attraction_matrix[matrix_point.x][matrix_point.y]

    def get_potential_matrix(self):
        """get an np array with the size of the grid and values who match the potential of each tile on the grid.
        """
        vec_func = np.vectorize(Tile.get_attraction, otypes=[np.int64])
        return vec_func(self.grid)

    def visualize_potential_matrix(self):
        pot_mat = self.get_potential_matrix()
        # Add a small constant to avoid division by zero
        pot_mat = np.log10(pot_mat + 1e-10)
        fig, ax = plt.subplots()
        im = plt.imshow(pot_mat, cmap='viridis', vmin=0)
        ax.grid(False)
        fig.colorbar(im)
        ax.set_title(label="Potential Matrix (logarithmic scale)")
        ax.axis("off")
        plt.show()

    def next_gen(self):
        """Perform a single iteration of the simulation.
           This is a generic function, which for each tile checks if there are any actions required ("get_context")
           Forwards the required parameters ("generate_context") to the cell, and preforms all of the actions sequentially.


        Returns:
            Grid: The new, result grid, after performing the iteration.
        """
        actions = {}
        # First iterate over the original board to calculate all necessary actions
        for x in range(self.height):
            for y in range(self.width):
                if (self.grid[x][y].cell):
                    cell_context = self.grid[x][y].cell.get_context()
                    actions[Point(x, y)] = self.grid[x][y].cell.get_actions(self.generate_context(
                        cell_context=cell_context, cell_location=Point(x, y)))

        # Copy the grid, and perform all of the actions.
        next_grid = deepcopy(self)
        for tile_actioned in actions:
            next_grid.exec_cell_actions(
                actions=actions[tile_actioned], cell_location=tile_actioned)
        return next_grid

    def generate_context(self, cell_context, cell_location: Point):
        """Create a dictionary with information about the grid, that can be passed to other objects.
           This class defines a clear api between the board and other entities using it. 

        Args:
            cell_context (list[ContextRequest]): List containing the types of requested information.
            cell_location (Point): The location of the requester. 

        Returns:
            dict: a dictionary with the information type as keys, and the requested information as values.
        """
        grid_context = {}
        attractions = {}
        neighbors_neighbors = {}

        if (ContextRequest.ATTRACTION_IN_NEIGHBORHOOD in cell_context):
            for neighbor_tile in get_tile_radius_outer_ring(location=cell_location, radius=1, max_width=self.width, max_height=self.height):
                # relative coords
                attractions[neighbor_tile -
                            cell_location] = self[neighbor_tile].attraction
            grid_context[ContextRequest.ATTRACTION_IN_NEIGHBORHOOD] = attractions

        if (ContextRequest.NUM_NEIGHBORS in cell_context):
            grid_context[ContextRequest.NUM_NEIGHBORS] = self.num_neighbors(
                cell_location)

        if (ContextRequest.NEIGHBORS_NEIGHBORS in cell_context):
            for neighbor_tile in get_tile_radius_outer_ring(location=cell_location, radius=1, max_width=self.width, max_height=self.height):
                neighbors_neighbors[neighbor_tile -
                                    cell_location] = self.num_neighbors(neighbor_tile)
            grid_context[ContextRequest.NEIGHBORS_NEIGHBORS] = neighbors_neighbors

        return grid_context

    def exec_cell_actions(self, actions: List[Action], cell_location: Point):
        """Perform the requested actions on the grid itself.

        Args:
            actions (List[Action]): List of actions to be performed.
            cell_location (Point): Position of the cell requesting the actions.
        """
        for action in actions:
            # From relative to absolute.
            new_location = action.dst + cell_location

            if action.type == ActionType.SPROUT and (not self[new_location].cell):
                self[new_location].cell = TipCell()
                self.stats.add_tip_cell()

            if action.type == ActionType.MIGRATE:

                # If moving to an empty tile, move the tip, reapply attraction.
                if (not self[new_location].cell):
                    self[new_location].cell = self[cell_location].cell

                # Tile is taken, merge with existing, override current cell with stalk.
                self[cell_location].cell = StalkCell()
                self.stats.add_stalk_cell()

            if action.type == ActionType.SPROUT:
                if (not self[action.dst + cell_location].cell):
                    self[action.dst + cell_location].cell = TipCell()
                    self.stats.add_tip_cell()

    def to_matrix(self):
        """Convert a grid to a numpy matrix, each cell type gets another color. 
           Used for visualization.

        Returns:
            numpy array
        """
        output = np.full(shape=(self.height, self.width),
                         fill_value=0, dtype=float)
        for x in range(self.height):
            for y in range(self.width):
                grid_cell = self.grid[x][y].cell
                if type(grid_cell) == StalkCell:
                    output[x][y] = 1
                if type(grid_cell) == TipCell:
                    output[x][y] = 2
                if type(grid_cell) == AttractorCell:
                    output[x][y] = 3

        return output

    def num_neighbors(self, location: Point) -> int:
        """Count the number of neighbors of a tile

        Args:
            location (Point): tile position.

        Returns:
            int: amount of neighbors.
        """
        num = 0
        for neighbor in get_tile_radius_outer_ring(location=location, radius=1, max_width=self.width, max_height=self.height):
            num += int(self[neighbor].cell != None)

        return num
