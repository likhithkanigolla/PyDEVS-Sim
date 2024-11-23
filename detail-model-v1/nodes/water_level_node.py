from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
import time

class WaterLevelNodeState:
    def __init__(self):
        self.data_aggregated = {}
        self.next_send_time = 1.0  # Initial time until the next data send

class WaterLevelNode(AtomicDEVS):
    def __init__(self, name=None):
        print(f"[{name}] Initializing WaterLevelNode.")
        AtomicDEVS.__init__(self, name)
        self.state = WaterLevelNodeState()
        self.timeLast = 0.0
        self.spi_inport = self.addInPort("spi_in")
        self.uart_inport = self.addInPort("uart_in")
        self.out_port = self.addOutPort("out")
        self.priority = 3
        
    def timeAdvance(self):
        print(f"[{self.name}] timeAdvance called. Next send time: {self.state.next_send_time}, timeLast: {self.timeLast}")
        return self.state.next_send_time - self.timeLast if self.state.data_aggregated else INFINITY
    
    def extTransition(self, inputs):
        print(f"[{self.name}] extTransition called with inputs: {inputs}")
        if self.spi_inport in inputs:
            self.state.data_aggregated['temperature'] = inputs[self.spi_inport]
            print(f"[{self.name}] Aggregated temperature data: {self.state.data_aggregated['temperature']}")
        if self.uart_inport in inputs:
            self.state.data_aggregated['ultrasonic'] = inputs[self.uart_inport]
            print(f"[{self.name}] Aggregated ultrasonic data: {self.state.data_aggregated['ultrasonic']}")
        self.timeLast = self.state.next_send_time  # Update timeLast
        return self.state
    
    def intTransition(self):
        print(f"[{self.name}] intTransition called.")
        self.timeLast = self.state.next_send_time  # Update timeLast
        self.state.next_send_time += 1.0
        return self.state
    
    def outputFnc(self):
        if self.state.data_aggregated:
            timestamp = str(int(time.time()))
            temp_value = str(self.state.data_aggregated.get('temperature', {}).get('temperature', ''))
            distance_value = str(self.state.data_aggregated.get('ultrasonic', {}).get('distance', ''))
            con_value = [timestamp, temp_value, distance_value]
            data_to_send = {
                "m2m:cin": {
                    "lbl": ["AE-WM-WL", "WM-WL-KH98-00", "V2.1.0", "WM-WD-V2.1.0"],
                    "con": con_value
                }
            }
            print(f"[{self.name}] Sending aggregated data: {data_to_send}")
            # Clear the aggregated data after sending
            self.state.data_aggregated = {}
            return {self.out_port: data_to_send}
        else:
            print(f"[{self.name}] No data to send.")
        return {}

    def __lt__(self, other):
        # Define comparison logic based on priority attribute
        return self.priority < other.priority