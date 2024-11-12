from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
import time

class WaterQualityNodeState:
    def __init__(self):
        self.data_aggregated = {}
        self.next_send_time = 1.0  # Initial time until the next data send

class WaterQualityNode(AtomicDEVS):
    def __init__(self, name):
        AtomicDEVS.__init__(self, name)
        self.state = WaterQualityNodeState()
        self.timeLast = 0.0  # Initialize timeLast
        self.spi_inport = self.addInPort("spi_in")
        self.adc_inport = self.addInPort("adc_in")
        self.outport = self.addOutPort("out")

    def timeAdvance(self):
        # Calculate the remaining time until the next send event
        print(f"[{self.name}] timeAdvance called. Next send time: {self.state.next_send_time}, timeLast: {self.timeLast}")
        return self.state.next_send_time - self.timeLast if self.state.data_aggregated else INFINITY

    def extTransition(self, inputs):
        # Update the state based on inputs from SPI and ADC
        if self.spi_inport in inputs:
            self.state.data_aggregated['temperature'] = inputs[self.spi_inport]
        if self.adc_inport in inputs:
            sensor_data = inputs[self.adc_inport]
            self.state.data_aggregated[sensor_data['sensor_id']] = sensor_data
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
            data_to_send = {
                "m2m:cin": {
                    "lbl": ["AE-WM-WD", "WM-WD-KH98-00", "V4.1.0", "WM-WD-V4.1.0"],
                    "con": f"{int(time.time())}, {self.state.data_aggregated}"
                }
            }
            print(f"[{self.name}] Sending aggregated data: {data_to_send}")
            # Clear the aggregated data after sending
            self.state.data_aggregated = {}
            return {self.outport: data_to_send}
        return {}