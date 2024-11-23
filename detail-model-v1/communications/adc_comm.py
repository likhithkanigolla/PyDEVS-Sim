from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY

class ADCState:
    def __init__(self):
        self.data = {}
        self.next_internal_time = INFINITY

class ADC(AtomicDEVS):
    def __init__(self, name, data_types=None):
        super().__init__(name)
        self.state = ADCState()
        self.data_types = data_types or []
        self.inports = {data_type: self.addInPort(f"in_{data_type}") for data_type in self.data_types}
        self.out_port = self.addout_port("out")
        self.priority = 2  # Priority for communication models

    def timeAdvance(self):
        return self.state.next_internal_time

    def extTransition(self, inputs):
        for data_type, port in self.inports.items():
            if port in inputs:
                self.state.data[data_type] = inputs[port]
                print(f"[{self.name}] Received {data_type} value: {inputs[port]}")
        self.state.next_internal_time = 0.0  # Schedule an immediate internal transition
        return self.state

    def outputFnc(self):
        # Forward the received data to the WaterQualityNode
        data_to_send = {"sensor_id": self.name, **self.state.data}
        print(f"[{self.name}] Forwarding data: {data_to_send}")
        self.state.next_internal_time = INFINITY  # Reset the internal time
        return {self.out_port: data_to_send}

    def intTransition(self):
        print(f"[{self.name}] intTransition called.")
        self.state.next_internal_time = INFINITY  # Reset the internal time
        return self.state

    def __lt__(self, other):
        # Define comparison logic based on priority attribute
        return self.priority < other.priority