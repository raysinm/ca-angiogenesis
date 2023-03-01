import numpy as np
np.set_printoptions(threshold= np.inf)

from Grid import Grid, Point
from Engine import Engine
import initial_states
from utils import visualize_statistics

# Create a an instance of the initial grid

#simple_grid = Grid(width=60, height=60, init_config=initial_states.init_config)
grid = Grid(width=60, height=60, init_config=initial_states.init_config_stalk_middle)
grid.visualize_potential_matrix()

# Create an instance of the engine, with the initial grid
engine = Engine(init_grid=grid, generations=81)

# Run the simulation
engine.run()

# Visualize the results: show simulation board
engine.visualize()

# Show some statistics about the simulation
engine.visualize_statistics()