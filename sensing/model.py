from pypdevs.DEVS import CoupledDEVS

from sensor import Sensor
from sink import Sink
from generator import Generator


class Model(CoupledDEVS):
    def __init__(self, num_to_generate):
        CoupledDEVS.__init__(self, "Model")
        self.generator = self.addSubModel(Generator(num_to_generate))
        self.sensor = self.addSubModel(Sensor())
        self.sink = self.addSubModel(Sink())
        self.connectPorts(self.generator.outport, self.sensor.inport)
        self.connectPorts(self.sensor.outport, self.sink.inport)