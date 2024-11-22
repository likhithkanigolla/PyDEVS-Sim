from pypdevs.DEVS import AtomicDEVS
import random

class TurbiditySensor(AtomicDEVS):
    def __init__(self, name):
        super(TurbiditySensor, self).__init__(name)
        self.state = 0
        self.sigma = 1
        self.outport = self.addOutPort("out")

    def intTransition(self):
        self.state = random.uniform(0, 100)
        return self.state

    def timeAdvance(self):
        return self.sigma

    def outputFnc(self):
        return {self.outport: self.state}