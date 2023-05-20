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
engine = Engine(init_grid=grid, generations=0)

# Run the simulation
engine.run()

# # Show the final result
# engine.visualize_final_result()

# # Visualize the simulation result
# engine.visualize()

# # Show the potential gradient
# grid.visualize_potential_matrix()

# # Show some statistics about the simulation
# engine.visualize_statistics()


#DEBUG Basic check if this function works (print the gif json) ---no idea if the gif is correct.

import json
import base64
from io import BytesIO
from PIL import Image

json_str = engine.generate_animation_in_json_gif()
json_obj = json.loads(json_str)
gif_base64 = json_obj['animation']
gif_bytes = base64.b64decode(gif_base64)

with open('animation.gif', 'wb') as f:
    f.write(gif_bytes)
gif_img = Image.open('animation.gif')

# gif_img.show()