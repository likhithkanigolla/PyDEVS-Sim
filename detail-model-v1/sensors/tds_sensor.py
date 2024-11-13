from pypdevs.DEVS import AtomicDEVS
import random

class TDSSensor(AtomicDEVS):
    def __init__(self, name):
        super().__init__(name)
        self.outport = self.addOutPort("out")
        self.priority = random.randint(1, 100)  # Example priority attribute

    def timeAdvance(self):
        return 5.0  # Every 5 seconds

    def outputFnc(self):
        tds_value = random.uniform(0, 1000)  # Random TDS value
        print(f"[{self.name}] Generating TDS value: {tds_value}")
        return {self.outport: tds_value}

    def __lt__(self, other):
        # Define comparison logic based on priority attribute
        return self.priority < other.priority