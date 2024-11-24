from pypdevs.DEVS import AtomicDEVS
import random

class TempSensor(AtomicDEVS):
    def __init__(self, name):
        super().__init__(name)
        self.in_port = self.addInPort("in_port")
        self.outport = self.addOutPort("outport")
        self.state = {"temp": 0}
        self.priority = 1
    
    def intTransition(self):
        self.state["temp"] = random.uniform(0, 100)
        return self.state
    
    def extTransition(self, inputs):
        return self.state 
    
    def outputFnc(self):
        print(f"[{self.name}] Generating temperature value: {self.state['temp']}")
        return {self.outport: self.state['temp']}
    
    def timeAdvance(self):
        return 5.0  # Every 5 seconds

    def __lt__(self, other):
        return self.priority < other.priority