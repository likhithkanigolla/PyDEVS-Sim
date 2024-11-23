from pypdevs.DEVS import AtomicDEVS
import random

class UltrasonicSensor(AtomicDEVS):
    def __init__(self, name):
        super(UltrasonicSensor, self).__init__(name)
        self.in_port = self.addInPort("in_port")
        self.outport = self.addOutPort("outport")
        self.state = {"distance": 0}
        self.priority = 1

    def intTransition(self):
        self.state["distance"] = random.uniform(0.5, 4.0)
        return self.state

    def extTransition(self, inputs):
        return self.state

    def outputFnc(self):
        return {self.outport: self.state["distance"]}

    def timeAdvance(self):
        return 1.0
    
    def __lt__(self, other):
            
            return self.priority < other.priority