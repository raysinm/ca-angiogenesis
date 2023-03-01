from utils import Point

#Stalk cells initiation options
initial_stalks_option1 = [Point(25, y) for y in range(60)]
initial_stalks_option2 = [Point(x,y) for x in range(0, 40) for y in range(20,60) if x == y-20]
initial_stalks_option3 = [Point(0, y) for y in range(60)]

#Attractor cells initiation options
initial_attractors_option1 = [Point(59, 15)]
initial_attractors_option2 = [Point(45, 15)]

# Putting together an init_config object
sanity_init_config = {'tip_cells': [Point(5,5)],
               'attractor_cells': initial_attractors_option1}

init_config_stalk_middle = { 'stalk_cells': initial_stalks_option1,
                             'attractor_cells': initial_attractors_option1}

init_config_stalk_diagonal = { 'stalk_cells': initial_stalks_option2,
                             'attractor_cells': initial_attractors_option1}

init_config_stalk_top = { 'stalk_cells': initial_stalks_option3,
                             'attractor_cells': initial_attractors_option1}