from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
import random
import time


from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
import random
import time

class WaterQualitySensorState:
    def __init__(self):
        self.next_reading_time = 1.0  
        self.sensor_id = "Sensor_01" 
        self.data_to_send = None  

class WaterQualitySensor(AtomicDEVS):
    def __init__(self, name, data_interval=1.0):
        AtomicDEVS.__init__(self, name)
        self.data_interval = data_interval
        self.state = WaterQualitySensorState()
        self.timeLast = 0.0
        self.inport = self.addInPort("in")
        self.outport = self.addOutPort("out")

    def timeAdvance(self):
        print(f"[{self.name}] timeAdvance called. Next reading time: {self.state.next_reading_time}, timeLast: {self.timeLast}")
        return self.state.next_reading_time - self.timeLast if self.state.data_to_send else INFINITY

    def intTransition(self):
        print(f"[{self.name}] intTransition called.")
        self.timeLast = self.state.next_reading_time 
        self.state.next_reading_time = self.timeLast + self.data_interval 
        self.generate_sensor_data()  # Generate new data
        return self.state

    def extTransition(self, inputs):
        print(f"[{self.name}] extTransition called with inputs: {inputs}")
        self.state.data_to_send = inputs[self.inport]
        self.state.next_reading_time = self.timeLast + self.data_interval
        return self.state

    def outputFnc(self):
        self.generate_sensor_data()  # Prepare data to send

        # Format the data as if it were a real POST request payload
        data = {
            "m2m:cin": {
                "lbl": ["AE-WM-WD", "WM-WD-KH98-00", "V4.1.0", "WM-WD-V4.1.0"],
                "con": f"[{self.state.data_to_send['timestamp']}, {self.state.data_to_send['pH']}, "
                       f"{self.state.data_to_send['turbidity']}, {self.state.data_to_send['tds']}]"
            }
        }
        
        print(f"[{self.name}] outputFnc called. Sending data: {data}")
        return {self.outport: data}  # Send data to the OneM2MInterface via outport

    def generate_sensor_data(self):
        # Generate sensor readings for pH, turbidity, and TDS
        self.state.data_to_send = {
            "sensor_id": self.state.sensor_id,
            "timestamp": int(time.time()),
            "pH": round(random.uniform(0, 14), 2),
            "turbidity": round(random.uniform(0, 100), 2),
            "tds": round(random.uniform(0, 1000), 2)
        }


# class WaterQualitySensorState:
#     def __init__(self):
#         self.next_reading_time = 1.0  
#         self.sensor_id = "Sensor_01" 
#         self.data_to_send = None  

# class WaterQualitySensor(AtomicDEVS):
#     def __init__(self, name, data_interval=1.0):
#         AtomicDEVS.__init__(self, name)
#         self.data_interval = data_interval
#         self.state = WaterQualitySensorState()
#         self.timeLast = 0.0
#         self.inport = self.addInPort("in")
#         self.outport = self.addOutPort("out")

       
#         self.state.data_to_send = {
#             "sensor_id": self.state.sensor_id,
#             "timestamp": int(time.time()),
#             "pH": random.uniform(0, 14),
#             "turbidity": random.uniform(0, 100),
#             "tds": random.uniform(0, 1000)
#         }

#     def timeAdvance(self):
#         print(f"[{self.name}] timeAdvance called. Next reading time: {self.state.next_reading_time}, timeLast: {self.timeLast}")
#         return self.state.next_reading_time - self.timeLast if self.state.data_to_send else INFINITY

#     def intTransition(self):
#         print(f"[{self.name}] intTransition called.")
#         self.timeLast = self.state.next_reading_time 
#         self.state.next_reading_time = self.timeLast + self.data_interval 
       
#         self.state.data_to_send = {
#             "sensor_id": self.state.sensor_id,
#             "timestamp": int(time.time()),
#             "pH": random.uniform(0, 14),
#             "turbidity": random.uniform(0, 100),
#             "tds": random.uniform(0, 1000)
#         }
#         return self.state

#     def extTransition(self, inputs):
#         print(f"[{self.name}] extTransition called with inputs: {inputs}")
#         self.state.data_to_send = inputs[self.inport]
#         self.state.next_reading_time = self.timeLast + self.data_interval
#         return self.state

#     def outputFnc(self):
#         self.state.data_to_send = {
#             "sensor_id": self.state.sensor_id,
#             "timestamp": int(time.time()),
#             "pH": random.uniform(0, 14),
#             "turbidity": random.uniform(0, 100),
#             "tds": random.uniform(0, 1000)
#         }
#         print(f"[{self.name}] outputFnc called. Sending data: {self.state.data_to_send}")
#         return {self.outport: self.state.data_to_send}