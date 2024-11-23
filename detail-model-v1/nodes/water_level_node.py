from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
import time

class WaterLevelNodeState:
    def __init__(self):
        self.data_aggregated = {}
        self.next_send_time = 1.0  # Interval for sending data

class WaterLevelNode(AtomicDEVS):
    def __init__(self, name):
        print(f"Initializing WaterLevelNode with name: {name}")
        AtomicDEVS.__init__(self, name)
        self.state = WaterLevelNodeState()
        self.timeLast = 0.0
        self.adc_inport = self.addInPort("adc_in")
        self.outport = self.addOutPort("out")
        self.priority = 3

    def timeAdvance(self):
        print(f"[{self.name}] timeAdvance called. Next send time: {self.state.next_send_time}, timeLast: {self.timeLast}")
        return self.state.next_send_time - self.timeLast if self.state.data_aggregated else INFINITY

    def extTransition(self, inputs):
        print(f"[{self.name}] extTransition called with inputs: {inputs}")
        if self.adc_inport in inputs:
            sensor_data = inputs[self.adc_inport]
            self.state.data_aggregated[sensor_data['sensor_id']] = sensor_data
            print(f"[{self.name}] Aggregated sensor data: {sensor_data}")
        self.timeLast = self.state.next_send_time
        return self.state

    def intTransition(self):
        print(f"[{self.name}] intTransition called.")
        self.timeLast = self.state.next_send_time
        self.state.next_send_time += 1.0
        return self.state

    def outputFnc(self):
        if self.state.data_aggregated:
            timestamp = str(int(time.time()))
            distance_value = str(self.state.data_aggregated.get('ADC', {}).get('distance', ''))
            con_value = [timestamp, distance_value]
            data_to_send = {
                "m2m:cin": {
                    "lbl": ["AE-WM-WL", "WM-WL-KH98-00", "V4.1.0", "WM-WL-V4.1.0"],
                    "con": con_value
                }
            }
            print(f"[{self.name}] Sending aggregated data: {data_to_send}")
            self.state.data_aggregated = {}
            return {self.outport: data_to_send}
        else:
            print(f"[{self.name}] No data to send.")
        return {}

    def __lt__(self, other):
        return self.priority < other.priority
