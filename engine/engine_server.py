import json
import importlib
from IPython.lib import deepreload
import grpc
import ca_simulator_pb2
import ca_simulator_pb2_grpc
from concurrent import futures

import types

import initial_states

import Cell
import Engine
import Grid
import utils

from pathlib import Path
# Default global config file
base_path = Path(__file__).parent
config_path = (base_path / "../engine/config.json").resolve()

class SimEngine(ca_simulator_pb2_grpc.SimEngineServicer):

    def RunSimulationGif(self, request, context):
        
        # ----- Updating parameters for simulation ----- #
        
        with open(config_path, 'r') as f:
            config_data = json.load(f)

        new_params = json.loads(request.params)
        for form_key, form_value in new_params.items():
            for param, numerical_value in form_value.items():
                if form_key in config_data['defaults'].keys() and numerical_value != None and numerical_value != '':
                    config_data['defaults'][form_key][param] = float(numerical_value)
        
        new_params_generations = new_params['graphics']['generations'] #TODO: fix me
        if new_params_generations != None and new_params_generations != '':
            config_data['graphics']['generations'] = int(new_params_generations)    
        # Write the updated data back to the file
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=4)

        # ----- Running simulation ----- #  #TODO: add an option to choose a different init board
        

        importlib.reload(utils)
        importlib.reload(Cell)
        importlib.reload(Grid)
        importlib.reload(Engine)
        
        #simple_grid = Grid(width=60, height=60, init_config=initial_states.init_config)
        grid = Grid.Grid(width=60, height=60,
                    init_config=initial_states.init_config_stalk_middle)

        # Create an instance of the engine, with the initial grid
        engine = Engine.Engine(init_grid=grid, generations=utils.GRAPHICS["generations"])

        # Run the simulation
        engine.run()


        # ----- Generating a gif and sending it back ----- #
        return ca_simulator_pb2.SimReply(simulation=engine.generate_animation_in_json_gif())

    
def serve():
    port='50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ca_simulator_pb2_grpc.add_SimEngineServicer_to_server(SimEngine(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Engine server running")
    server.wait_for_termination()

if __name__ == "__main__":
    #TODO: context log config?
    serve()


        