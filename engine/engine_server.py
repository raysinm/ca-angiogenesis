import json

import grpc
import ca_simulator_pb2
import ca_simulator_pb2_grpc
from concurrent import futures

import initial_states
from Engine import Engine
from Grid import Grid
from utils import DEFAULTS, GRAPHICS

class SimEngine(ca_simulator_pb2_grpc.SimEngineServicer):

    def RetSimulationGif(self, request, context):
        
        # ----- Updating parameters for simulation ----- #
        
        with open("./config.json", 'r') as f:
            config_data = json.load(f)

        new_params = {
        'tip_cell': {
        "p_migrate": request.params.get('tip_cell_p_migrate')       #! Does 'get' work like this? 
        },
        'attractor_cell' : {
            "attraction_generated": request.params.get('attractor_cell_attraction_generated')
        },
        'stalk_cell' : {
            "p_sprout": request.params.get('stalk_cell_p_sprout')
        },
        'attraction' : {
            "decay_coef": request.params.get('attraction_decay_coef'),
            "update_precision": request.params.get('attraction_update_precision')
        },
        'graphics': {
            'generations' : request.params.get('graphics_generations')
        } 
        }
        for form_key, form_value in new_params.items():
            for param, numerical_value in form_value.items():
                if form_key in config_data['defaults'].keys() and numerical_value != None and numerical_value != '':
                    config_data['defaults'][form_key][param] = float(numerical_value)
        
        new_params_generations = new_params['graphics']['generations'] #TODO: fix me
        if new_params_generations != None and new_params_generations != '':
            config_data['graphics']['generations'] = int(new_params_generations)    
        # Write the updated data back to the file
        with open("./config.json", 'w') as f:
            json.dump(config_data, f, indent=4)

        # ----- Running simulation ----- #  #TODO: add an option to choose a different init board
        
        #simple_grid = Grid(width=60, height=60, init_config=initial_states.init_config)
        grid = Grid(width=60, height=60,
                    init_config=initial_states.init_config_stalk_middle)

        # Create an instance of the engine, with the initial grid
        engine = Engine(init_grid=grid, generations=GRAPHICS["generations"])

        # Run the simulation
        engine.run()


        # ----- Generating a gif and sending it back ----- #
        return ca_simulator_pb2.SimReply(simulation=engine.generate_animation_in_json_gif())

    
    def serve():
        port='50050'
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        ca_simulator_pb2_grpc.add_SimEngineServicer_to_server(SimEngine(), server)
        server.add_insecure_port('[::]' + port)
        server.start()
        server.wait_for_termination()

    if __name__ == "__main__":
        #TODO: context log config?
        serve()


        