from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY

class SinkState(object):
    def __init__(self):
        self.received = float("-inf")


class Sink(AtomicDEVS):
    def __init__(self):
        AtomicDEVS.__init__(self, "Sink")
        self.state = SinkState()
        self.processing_time = 1.0
        self.inport = self.addInPort("input")
        print("Sink initialized with processing time:", self.processing_time)


    def timeAdvance(self):
        if self.state is None:
            print("Time advance called: state is None, returning INFINITY")
            return INFINITY
        else:
            print("Time advance called: state is not None, returning processing time:", self.processing_time)
            return self.processing_time


    def extTransition(self, inputs):
        self.state.received = inputs[self.inport]
        print("External transition called: received input:", self.state.received)
        return self.state


    def intTransition(self):
        print("Internal transition called: current state received:", self.state.received)
        return self.state