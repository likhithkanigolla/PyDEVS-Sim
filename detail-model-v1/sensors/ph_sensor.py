from pypdevs.DEVS import AtomicDEVS
import random

class PHSensor(AtomicDEVS):
    def __init__(self, name):
        super().__init__(name)
        self.inport = self.addInPort("in_port") 
        self.out_port = self.addOutPort("out_port")
        self.state = {"ph": 0}
        self.priority = 1
    
    def intTransition(self):
        self.state["ph"] = random.uniform(0, 14)
        return self.state
    
    def extTransition(self, inputs):
        return self.state

    def outputFnc(self):
        print(f"[{self.name}] Generating PH value: {self.state['ph']}")
        return {self.out_port: self.state['ph']}

    def timeAdvance(self):
        return 5.0  
    
    def __lt__(self, other):
        return self.priority < other.priority