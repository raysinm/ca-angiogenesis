import grpc
from . import ca_simulator_pb2
from . import ca_simulator_pb2_grpc

def run(new_params, manual_run:int=0):
    loc = 'engine-server'
    if (manual_run==1):
        loc = 'localhost'
        
    with grpc.insecure_channel(f'{loc}:50051') as channel:
        stub = ca_simulator_pb2_grpc.SimEngineStub(channel)
        response = stub.RunSimulationGif(ca_simulator_pb2.SimRequest(params=new_params))
        return response.simulation
    

if __name__ == '__main__':
    #TODO: config logging?
    new_params_dummy = "{}"
    run(new_params_dummy)