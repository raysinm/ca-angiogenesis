import numpy as np
np.set_printoptions(threshold= np.inf)

from Grid import Grid, Point
from Engine import Engine
import initial_states

# Create a an instance of the initial grid

#simple_grid = Grid(width=30, height=30, init_config=initial_states.init_config)
grid = Grid(width=60, height=60, init_config=initial_states.init_config_stalk_middle)
grid.visualize_potential_matrix()

# Create an instance of the engine, with the initial grid
engine = Engine(init_grid=grid, generations=36)

# Run the simulation
engine.run()

# Visualize the results: show simulation board, and a map of the board initial potential.
engine.visualize()