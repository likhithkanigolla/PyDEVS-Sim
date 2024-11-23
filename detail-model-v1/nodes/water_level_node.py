from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
import time

class WaterLevelNodeState:
    def __init__(self):
        self.data_aggregated = {}
        self.next_send_time = 1.0  # Initial time until the next data send

class WaterLevelNode(AtomicDEVS):
    def __init__(self, name):
        print(f"Initializing WaterLevelNode with name: {name}")
        AtomicDEVS.__init__(self, name)
        self.state = WaterLevelNodeState()
        self.timeLast = 0.0  # Initialize timeLast
        self.adc_inport = self.addInPort("adc_inport")
        self.outport = self.addOutPort("out")
        self.priority = 3  # Priority for nodes

    def timeAdvance(self):
        # Calculate the remaining time until the next send event
        print(f"[{self.name}] timeAdvance called. Next send time: {self.state.next_send_time}, timeLast: {self.timeLast}")
        return self.state.next_send_time - self.timeLast if self.state.data_aggregated else INFINITY

    def extTransition(self, inputs):
        # Update the state based on inputs from ADC
        print(f"[{self.name}] extTransition called with inputs: {inputs}")
        if self.adc_inport in inputs:
            sensor_data = inputs[self.adc_inport]
            self.state.data_aggregated[sensor_data['sensor_id']] = sensor_data
            print(f"[{self.name}] Aggregated sensor data: {sensor_data}")
        self.timeLast = self.state.next_send_time  # Update timeLast
        return self.state

    def intTransition(self):
        # Schedule the next send time
        print(f"[{self.name}] intTransition called.")
        self.timeLast = self.state.next_send_time  # Update timeLast
        self.state.next_send_time += 1.0
        return self.state

    def outputFnc(self):
        # Only send data if there is aggregated data
        if self.state.data_aggregated:
            timestamp = str(int(time.time()))
            distance_value = str(self.state.data_aggregated.get('ADC_WaterLevel', {}).get('distance', ''))
            con_value = [timestamp, distance_value]
            data_to_send = {
                "m2m:cin": {
                    "lbl": ["AE-WM-WL", "WM-WL-KH98-00", "V4.1.0", "WM-WL-V4.1.0"],
                    "con": con_value
                }
            }
            print(f"[{self.name}] Sending aggregated data: {data_to_send}")
            # Clear the aggregated data after sending
            self.state.data_aggregated = {}
            return {self.outport: data_to_send}
        else:
            print(f"[{self.name}] No data to send.")
        return {}

    def __lt__(self, other):
        # Define comparison logic based on priority attribute
        return self.priority < other.priority