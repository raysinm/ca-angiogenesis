import initial_states
from Engine import Engine
from Grid import Grid
import numpy as np
from utils import DEFAULTS, GRAPHICS

def vis():
    
    #simple_grid = Grid(width=60, height=60, init_config=initial_states.init_config)
    grid = Grid(width=60, height=60,
                init_config=initial_states.init_config_stalk_middle)

    # Create an instance of the engine, with the initial grid
    engine = Engine(init_grid=grid, generations=GRAPHICS["generations"])

    # Run the simulation
    engine.run()

    return engine.generate_animation_in_html()

