import initial_states
from Engine import Engine
from Grid import Grid, Point
import numpy as np
np.set_printoptions(threshold=np.inf)


# Create a an instance of the initial grid

#simple_grid = Grid(width=60, height=60, init_config=initial_states.init_config)
grid = Grid(width=60, height=60,
            init_config=initial_states.init_config_stalk_middle)

# Create an instance of the engine, with the initial grid
engine = Engine(init_grid=grid, generations=81)

# Run the simulation
engine.run()

# Show the final result
engine.visualize_final_result()

# Visualize the simulation result
engine.visualize()

# Show the potential gradient
grid.visualize_potential_matrix()

# Show some statistics about the simulation
engine.visualize_statistics()
