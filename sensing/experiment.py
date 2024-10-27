from pypdevs.simulator import Simulator
from model import Model
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    values = []
    num_to_generate = 10

    logging.debug("Starting the model with num_to_generate = %d", num_to_generate)
    model = Model(num_to_generate)
    logging.debug("Model Loaded num_to_generate = %d", num_to_generate)
    
    sim = Simulator(model)
    logging.debug("Simulator Loaded")
    
    sim.setClassicDEVS()
    logging.debug("Classic DEVS set")
    
    sim.setVerbose()
    logging.debug("Verbose mode set")
    
    sim.setTerminationTime(5)
    logging.debug("Termination time set to 5")
    
    logging.debug("Starting simulation")
    sim.simulate()
    logging.debug("Simulation finished")
