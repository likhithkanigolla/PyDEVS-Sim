from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
import random

class OneM2MInterfaceState:
    def __init__(self):
        self.processing_time = 0.0 
        self.data_to_send = None

class OneM2MInterface(AtomicDEVS):
    def __init__(self, server_url, username, password, simulated_delay=1.0):
        AtomicDEVS.__init__(self, "OneM2MInterface")
        self.server_url = server_url
        self.auth = (username, password)
        self.simulated_delay = simulated_delay
        self.state = OneM2MInterfaceState()
        self.inport = self.addInPort("in")
        self.outport = self.addOutPort("out")

    def timeAdvance(self):
        if self.state.data_to_send is None:
            return INFINITY 
        return self.state.processing_time - self.timeLast

    def extTransition(self, inputs):
        self.state.data_to_send = inputs[self.inport]
        self.state.processing_time = self.timeLast + self.simulated_delay
        return self.state

    def outputFnc(self):
        sent_data = self.state.data_to_send
        self.state.data_to_send = None
        print(f"OneM2M Interface simulated sending: {sent_data}")
        return {self.outport: sent_data}

    def intTransition(self):
        self.state.processing_time = INFINITY 
        return self.state