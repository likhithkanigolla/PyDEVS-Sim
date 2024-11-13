from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY

class ADCState:
    def __init__(self):
        self.ph_value = None
        self.tds_value = None
        self.next_internal_time = INFINITY

class ADC(AtomicDEVS):
    def __init__(self, name):
        super().__init__(name)
        self.state = ADCState()
        self.inport_ph = self.addInPort("in_ph")
        self.inport_tds = self.addInPort("in_tds")
        self.outport = self.addOutPort("out")
        self.priority = 1  # Example priority attribute

    def timeAdvance(self):
        return self.state.next_internal_time

    def extTransition(self, inputs):
        print(f"[{self.name}] extTransition called with inputs: {inputs}")
        if self.inport_ph in inputs:
            self.state.ph_value = inputs[self.inport_ph]
            print(f"[{self.name}] Received pH value: {self.state.ph_value}")
        if self.inport_tds in inputs:
            self.state.tds_value = inputs[self.inport_tds]
            print(f"[{self.name}] Received TDS value: {self.state.tds_value}")
        self.state.next_internal_time = 0.0  # Schedule an immediate internal transition
        return self.state

    def outputFnc(self):
        # Forward the received data to the WaterQualityNode
        data_to_send = {
            "sensor_id": "ADC",
            "ph": self.state.ph_value,
            "tds": self.state.tds_value
        }
        print(f"[{self.name}] Forwarding data: {data_to_send}")
        self.state.next_internal_time = INFINITY  # Reset the internal time
        return {self.outport: data_to_send}

    def intTransition(self):
        print(f"[{self.name}] intTransition called.")
        self.state.next_internal_time = INFINITY  # Reset the internal time
        return self.state

    def __lt__(self, other):
        # Define comparison logic based on priority attribute
        return self.priority < other.priority