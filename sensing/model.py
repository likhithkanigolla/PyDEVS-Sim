from pypdevs.DEVS import CoupledDEVS

from sensor import Sensor
from sink import Sink
from generator import Generator


class Model(CoupledDEVS):
    def __init__(self, num_to_generate):
        CoupledDEVS.__init__(self, "Model")
        print("Model Loaded num_to_generate here = ", num_to_generate)
        
        print("Initializing Generator with num_to_generate =", num_to_generate)
        self.generator = self.addSubModel(Generator(num_to_generate))
        
        print("Initializing Sensor")
        self.sensor = self.addSubModel(Sensor())
        
        print("Initializing Sink")
        self.sink = self.addSubModel(Sink())
        
        print("Connecting Generator's outport to Sensor's inport")
        self.connectPorts(self.generator.outport, self.sensor.inport)
        
        print("Connecting Sensor's outport to Sink's inport")
        self.connectPorts(self.sensor.outport, self.sink.inport)
        
        print("Model initialization complete")