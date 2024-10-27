from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY

class SinkState(object):
    def __init__(self):
        self.received = float("-inf")


class Sink(AtomicDEVS):
    def __init__(self):
        AtomicDEVS.__init__(self,"Sink")
        self.state = SinkState()
        self.processing_time = 1.0
        self.inport = self.addInPort("input")


    def timeAdvance(self):
        if self.state is None:
            return INFINITY
        else:
            return self.processing_time


    def extTransition(self, inputs):
        self.state.received = inputs[self.inport]
        return self.state


    def intTransition(self):
        return self.state