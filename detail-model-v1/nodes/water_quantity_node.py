from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
import time

class WaterQuantityTypeOneState:
    def __init__(self):
        self.data = {}
        self.next_internal_time = 1.0

class WaterQuantityTypeOne(AtomicDEVS):
    def __init__(self, name=None):
        print(f"[{name}] Initializing WaterQuantityTypeOne.")
        AtomicDEVS.__init__(self, name)
        self.state = WaterQuantityTypeOneState()
        self.time_last = 0.0  # Initialize time_last as a float
        self.gpio_inport = self.addInPort("gpio_in")
        self.out_port = self.addOutPort("out")
        self.priority = 3

    def timeAdvance(self):
        print(f"[{self.name}] Time advance called. Next internal time: {self.state.next_internal_time}, time_last: {self.time_last}")
        return self.state.next_internal_time - self.time_last if self.state.data else INFINITY

    def extTransition(self, inputs):
        print(f"[{self.name}] External transition called. Inputs: {inputs}")
        if self.gpio_inport in inputs:
            self.state.data = inputs[self.gpio_inport]
            print(f"[{self.name}] Received data: {self.state.data}")
        self.time_last = self.state.next_internal_time  # Update time_last
        return self.state

    def outputFnc(self):
        if self.state.data:
            timestamp = str(int(time.time()))
            pulse_data = str(self.state.data.get('pulse', ''))
            con_value = [timestamp, pulse_data]
            data_to_send = {
                "m2m:cin": {
                    "lbl": ["AE-WM-WD", "WM-WD-KH98-00", "V1.0.0", "WM-WL-V1.0.0"],
                    "con": con_value
                }
            }
            print(f"[{self.name}] Sending data: {data_to_send}")
            return {self.out_port: data_to_send}
        else:
            print(f"[{self.name}] No data to send.")
            return {}

    def intTransition(self):
        print(f"[{self.name}] Internal transition called.")
        self.time_last = self.state.next_internal_time  # Update time_last
        self.state.next_internal_time += 1.0
        return self.state

    def __lt__(self, other):
        return self.priority < other.priority