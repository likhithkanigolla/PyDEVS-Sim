# Camera Sensor which captures the image and identify the numbers and send the integer to the controller
from pypdevs.DEVS import AtomicDEVS
import random


class CameraSensor(AtomicDEVS):
    def __init__(self, name):
        super().__init__(name)
        self.state = "idle"
        self.image_data = None
        self.number_detected = None
        self.processing_time = random.uniform(1, 5)
        self.addInPort("in_port")
        self.addOutPort("outport")

    def intTransition(self):
        if self.state == "processing":
            self.state = "idle"
            self.number_detected = self.generate_random_number()
            return self.state
        return self.state

    def extTransition(self, inputs):
        if self.state == "idle":
            self.image_data = inputs["in_port"]
            self.state = "processing"
        return self.state

    def outputFnc(self):
        if self.state == "processing":
            return {"outport": self.number_detected}
        return {}

    def timeAdvance(self):
        if self.state == "processing":
            return self.processing_time
        return float('inf')

    def generate_random_number(self):
        # Generate a random 6-digit integer
        return random.randint(100000, 999999)
