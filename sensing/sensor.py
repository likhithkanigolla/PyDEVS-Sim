from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY

class SensorState(object):
    def __init__(self):
        self.measurement = float("-inf")
        self.timestamp = float("-inf")


class Sensor(AtomicDEVS):
    def __init__(self):
        AtomicDEVS.__init__(self,"Sensor")
        self.state = SensorState()
        self.processing_time = 1.0
        self.inport = self.addInPort("input")
        self.outport = self.addOutPort("output")


    def timeAdvance(self):
        if self.state is None:
            return INFINITY
        else:
            return self.processing_time


    def outputFnc(self):
        return { self.outport: { self.state } }


    def extTransition(self, inputs):
        self.state.timestamp = list(inputs[self.inport])[0]
        self.state.measurement = list(inputs[self.inport])[1]
        return self.state


    def intTransition(self):
        return self.state
