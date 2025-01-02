from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
import time

class WaterQualityNodeState:
    def __init__(self):
        self.data_aggregated = {}
        self.next_send_time = 1.0  # Initial time until the next data send

class WaterQualityNode(AtomicDEVS):
    def __init__(self, name):
        print(f"Initializing WaterQualityNode with name: {name}")
        AtomicDEVS.__init__(self, name)
        self.state = WaterQualityNodeState()
        self.timeLast = 0.0  # Initialize timeLast

        # ESP32 Pin Definitions
        self.pin_map = {
            "GPIO_0": {"category": "Touch", "type": "Reserved for boot mode"},
            "GPIO_1": {"category": "UART", "type": "TX"},
            "GPIO_2": {"category": ["Digital I/O", "Touch"], "type": "General-purpose"},
            "GPIO_3": {"category": "UART", "type": "RX"},
            "GPIO_4": {"category": ["Digital I/O", "Touch"], "type": "General-purpose"},
            "GPIO_5": {"category": "SPI", "type": "General-purpose"},
            "GPIO_12": {"category": ["Digital I/O", "Touch"], "type": "General-purpose"},
            "GPIO_13": {"category": ["Digital I/O", "Touch"], "type": "General-purpose"},
            "GPIO_14": {"category": ["Digital I/O", "Touch"], "type": "General-purpose"},
            "GPIO_15": {"category": "Digital I/O", "type": "General-purpose"},
            "GPIO_16": {"category": ["PWM", "UART"], "type": "General-purpose"},
            "GPIO_17": {"category": ["PWM", "UART"], "type": "General-purpose"},
            "GPIO_18": {"category": ["PWM", "SPI"], "type": "SPI Clock (SCK)"},
            "GPIO_19": {"category": ["PWM", "SPI"], "type": "SPI MISO connected to Temp Sensor"},
            "GPIO_21": {"category": "PWM", "type": "General-purpose"},
            "GPIO_22": {"category": "I2C", "type": "I2C SCL"},
            "GPIO_23": {"category": ["PWM", "SPI"], "type": "SPI MOSI"},
            "GPIO_25": {"category": "DAC", "type": "DAC Channel"},
            "GPIO_26": {"category": "DAC", "type": "DAC Channel"},
            "GPIO_27": {"category": ["I2C", "Touch"], "type": "General-purpose"},
            "GPIO_32": {"category": ["Analog Pins (ADC)", "RTC GPIOs"], "type": "ADC Channel connected to pH Sensor"},
            "GPIO_33": {"category": ["Analog Pins (ADC)", "RTC GPIOs"], "type": "ADC Channel connected to TDS Sensor"},
            "GPIO_34": {"category": "Analog Pins (ADC)", "type": "ADC Channel"},
            "GPIO_35": {"category": "Analog Pins (ADC)", "type": "ADC Channel"},
            "GPIO_36": {"category": "Analog Pins (ADC)", "type": "ADC Channel"},
            "GPIO_39": {"category": "Analog Pins (ADC)", "type": "ADC Channel"},
            "3V3": {"category": "Power", "type": "Power Supply (external connection assumed)"},
            "GND": {"category": "Ground", "type": "Ground (external connection assumed)"}
        }

        # Ports
        self.temp_inport = self.addInPort("temp_in")
        self.ph_inport = self.addInPort("ph_in")
        self.tds_inport = self.addInPort("tds_in")
        self.outport = self.addOutPort("out")

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
