from pypdevs.DEVS import AtomicDEVS
import random

class CurrentSensor(AtomicDEVS):
    def __init__(self, name):
        super(CurrentSensor, self).__init__(name)
        self.in_port = self.addInPort("in_port")
        self.out_port = self.addOutPort("out_port")
        self.state = 0

    def intTransition(self):
        self.state = random.uniform(0, 100)
        return self.state

    def extTransition(self, inputs):
        if self.in_port in inputs:
            self.state = inputs[self.in_port]
        return self.state

    def outputFnc(self):
        return {self.out_port: self.state}

    def timeAdvance(self):
        return 1