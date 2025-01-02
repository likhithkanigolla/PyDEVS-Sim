from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
import time


class WaterQualityNodeState:
    def __init__(self):
        self.data_aggregated = {}
        self.next_send_time = 1.0  # Initial time until the next data send

class WaterQualityNode(AtomicDEVS):
    def __init__(self, name, esp_pins):
        print(f"Initializing WaterQualityNode with name: {name}")
        AtomicDEVS.__init__(self, name)
        self.state = WaterQualityNodeState()
        self.timeLast = 0.0  # Initialize timeLast
        self.pins = esp_pins  # Use the provided ESP pin configuration

        # Ports
        self.temp_inport = self.addInPort(f"temp_in_{self.pins['SPI'][0]}")  # Using first ADC pin for temperature
        self.ph_inport = self.addInPort(f"ph_in_{self.pins['ADC'][1]}")  # Using second ADC pin for pH
        self.tds_inport = self.addInPort(f"tds_in_{self.pins['ADC'][2]}")  # Using third ADC pin for TDS
        self.turbudity_inport = self.addInPort(f"turbidity_in_{self.pins['ADC'][3]}")  # Using fourth ADC pin for turbidity
        self.outport = self.addOutPort("out")

        # External Power Pins (3V3 and GND)
        self.power_3v3 = self.pins["POWER"]["3V3"]
        self.power_GND = self.pins["POWER"]["GND"]

        self.priority = 3  # Priority for nodes

    def timeAdvance(self):
        print(f"[{self.name}] timeAdvance called. Next send time: {self.state.next_send_time}, timeLast: {self.timeLast}")
        return self.state.next_send_time - self.timeLast if self.state.data_aggregated else INFINITY

    def extTransition(self, inputs):
        print(f"[{self.name}] extTransition called with inputs: {inputs}")
        if self.temp_inport in inputs:
            self.state.data_aggregated["temperature"] = inputs[self.temp_inport]
        if self.ph_inport in inputs:
            self.state.data_aggregated["pH"] = inputs[self.ph_inport]
        if self.tds_inport in inputs:
            self.state.data_aggregated["TDS"] = inputs[self.tds_inport]
        if self.turbudity_inport in inputs:
            self.state.data_aggregated["turbidity"] = inputs[self.turbudity_inport]
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
            data_to_send = {
                "m2m:cin": {
                    "lbl": ["AE-WM-WD", "WM-WD-KH98-00", "V4.1.0", "WM-WD-V4.1.0"],
                    "con": [
                        timestamp,
                        self.state.data_aggregated.get("pH", ""),
                        self.state.data_aggregated.get("TDS", ""),
                        self.state.data_aggregated.get("temperature", "")
                    ]
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
