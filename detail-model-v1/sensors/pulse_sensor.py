from pypdevs.DEVS import AtomicDEVS
import random

class PulseSensor(AtomicDEVS):
    def __init__(self, name):
        super().__init__(name)
        self.state = 0
        self.sigma = random.uniform(0.5, 1.5)

    def intTransition(self):
        self.state = random.randint(0, 1)
        self.sigma = random.uniform(0.5, 1.5)
        return self.state

    def timeAdvance(self):
        return self.sigma

    def outputFnc(self):
        return {"pulse": self.state}