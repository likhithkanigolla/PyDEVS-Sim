from pypdevs.DEVS import AtomicDEVS
import random

class TempSensor(AtomicDEVS):
    def __init__(self, name):
        super().__init__(name)
        self.outport = self.addOutPort("out")
        self.priority = 1

    def timeAdvance(self):
        return 5.0  # Every 5 seconds

    def outputFnc(self):
        temp_value = random.uniform(0, 100)  # Random temperature
        print(f"[{self.name}] Generating temperature value: {temp_value}")
        return {self.outport: temp_value}

    def __lt__(self, other):
        
        return self.priority < other.priority