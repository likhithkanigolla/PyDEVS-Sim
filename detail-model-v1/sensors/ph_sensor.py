from pypdevs.DEVS import AtomicDEVS
import random

class PHSensor(AtomicDEVS):
    def __init__(self, name):
        super().__init__(name)
        self.outport = self.addOutPort("out")
        self.priority = 1

    def timeAdvance(self):
        return 5.0  # Every 5 seconds

    def outputFnc(self):
        ph_value = random.uniform(0, 14)  # Random pH value
        print(f"[{self.name}] Generating pH value: {ph_value}")
        return {self.outport: ph_value}

    def __lt__(self, other):
        
        return self.priority < other.priority