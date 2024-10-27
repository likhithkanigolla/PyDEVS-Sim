from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
import random
import time

class WaterQualitySensorState:
    def __init__(self):
        self.next_reading_time = 0.0
        self.data_to_send = {
            "sensor_id": self.state.sensor_id,
            "timestamp": int(time.time()),
            "pH": random.uniform(0, 14),
            "turbidity": random.uniform(0, 100),
            "tds": random.uniform(0, 1000)
        }

class WaterQualitySensor(AtomicDEVS):
    def __init__(self, name, data_interval=1.0):
        AtomicDEVS.__init__(self, name)
        self.data_interval = data_interval
        self.state = WaterQualitySensorState()
        self.timeLast = 0.0  # Initialize timeLast
        self.inport = self.addInPort("in")
        self.outport = self.addOutPort("out")

    def timeAdvance(self):
        print(f"[{self.name}] timeAdvance called. Next reading time: {self.state.next_reading_time}, timeLast: {self.timeLast}")
        if self.state.data_to_send is None:
            return INFINITY
        return self.state.next_reading_time - self.timeLast

    def extTransition(self, inputs):
        print(f"[{self.name}] extTransition called with inputs: {inputs}")
        self.state.data_to_send = inputs[self.inport]
        self.state.next_reading_time = self.timeLast + self.data_interval
        return self.state

    def outputFnc(self):
        # sent_data = {
        #     "sensor_id": self.state.sensor_id,
        #     "timestamp": int(time.time()),
        #     "pH": random.uniform(0, 14),
        #     "turbidity": random.uniform(0, 100),
        #     "tds": random.uniform(0, 1000)
        # }
        self.state.data_to_send = {
            "sensor_id": self.state.sensor_id,
            "timestamp": int(time.time()),
            "pH": random.uniform(0, 14),
            "turbidity": random.uniform(0, 100),
            "tds": random.uniform(0, 1000)
        }
        print(f"[{self.name}] outputFnc called. Sending data: {self.state.data_to_send}")
        return {self.outport: self.state.data_to_send}

    def intTransition(self):
        print(f"[{self.name}] intTransition called.")
        self.timeLast = self.state.next_reading_time  # Update timeLast
        self.state.next_reading_time = INFINITY
        return self.state