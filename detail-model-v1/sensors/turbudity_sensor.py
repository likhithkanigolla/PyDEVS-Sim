from pypdevs.DEVS import AtomicDEVS
import random

class TurbiditySensor(AtomicDEVS):
    def __init__(self, name):
        super(TurbiditySensor, self).__init__(name)
        self.in_port = self.addInPort("in_port")
        self.out_port = self.addOutPort("out_port")
        self.state = {"turbidity": 0}
        self.priority = 1
    
    def intTransition(self):
        self.state["turbidity"] = random.uniform(0, 100)
        return self.state
    
    def extTransition(self, inputs):
        return self.state
    
    def outputFnc(self):
        print(f"[{self.name}] Generating turbidity value: {self.state['turbidity']}")
        return {self.out_port: self.state['turbidity']}
    
    def timeAdvance(self):
        return 5.0
    
    def __lt__(self, other):
        return self.priority < other.priority
    