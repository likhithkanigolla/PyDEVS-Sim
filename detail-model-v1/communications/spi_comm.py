from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY

class SPIState:
    def __init__(self):
        self.temp_value = None
        self.next_internal_time = INFINITY

class SPI(AtomicDEVS):
    def __init__(self, name):
        super().__init__(name)
        self.state = SPIState()
        self.inport_temp = self.addInPort("in_temp")
        self.outport = self.addOutPort("out")
        self.priority = 2

    def timeAdvance(self):
        return self.state.next_internal_time

    def extTransition(self, inputs):
        print(f"[{self.name}] extTransition called with inputs: {inputs}")
        if self.inport_temp in inputs:
            self.state.temp_value = inputs[self.inport_temp]
            print(f"[{self.name}] Received temperature value: {self.state.temp_value}")
        self.state.next_internal_time = 0.0  # Schedule an immediate internal transition
        return self.state

    def outputFnc(self):
        # Forward the received data to the WaterQualityNode
        data_to_send = {
            "sensor_id": "SPI",
            "temperature": self.state.temp_value
        }
        print(f"[{self.name}] Forwarding data: {data_to_send}")
        self.state.next_internal_time = INFINITY  # Reset the internal time
        return {self.outport: data_to_send}

    def intTransition(self):
        print(f"[{self.name}] intTransition called.")
        self.state.next_internal_time = INFINITY  # Reset the internal time
        return self.state

    def __lt__(self, other):
        
        return self.priority < other.priority