# import sys
import numpy as np
# numpy.set_printoptions(threshold=sys.maxsize)
np.set_printoptions(threshold= np.inf)

from Grid import Grid, Point
from Engine import Engine
import initial_states

init_config = {'stalk_cells': [Point(0,0)],
                'tip_cells': [Point(1,1)],
               'attractor_cells': initial_states.Attractors_small2}
grid = Grid(width=15, height=15, init_config=init_config)
engine = Engine(init_grid=grid, generations=100)
engine.run()