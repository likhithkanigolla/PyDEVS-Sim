from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
import random
import time

class WaterQualitySensorState:
    def __init__(self, sensor_id):
        self.sensor_id = sensor_id
        self.next_reading_time = 0.0

class WaterQualitySensor(AtomicDEVS):
    def __init__(self, sensor_id, data_interval=3600):
        AtomicDEVS.__init__(self, f"WaterQualitySensor_{sensor_id}")
        self.state = WaterQualitySensorState(sensor_id)
        self.data_interval = data_interval
        self.outport = self.addOutPort("out")

    def timeAdvance(self):
        if self.state.next_reading_time == INFINITY:
            return INFINITY
        return self.state.next_reading_time - self.timeLast

    def outputFnc(self):
        sensor_data = {
            "sensor_id": self.state.sensor_id,
            "timestamp": int(time.time()),
            "pH": random.uniform(0, 14),
            "turbidity": random.uniform(0, 100),
            "tds": random.uniform(0, 1000)
        }
        return {self.outport: sensor_data}

    def intTransition(self):
        self.state.next_reading_time = self.timeLast + self.data_interval
        return self.state