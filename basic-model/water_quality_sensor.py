from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY

class WaterQualitySensorState:
    def __init__(self):
        self.next_reading_time = 0.0
        self.data_to_send = None

class WaterQualitySensor(AtomicDEVS):
    def __init__(self, name, data_interval=1.0):
        AtomicDEVS.__init__(self, name)
        self.data_interval = data_interval
        self.state = WaterQualitySensorState()
        self.timeLast = 0.0  # Initialize timeLast
        self.inport = self.addInPort("in")
        self.outport = self.addOutPort("out")

    def timeAdvance(self):
        if self.state.data_to_send is None:
            return INFINITY
        return self.state.next_reading_time - self.timeLast

    def extTransition(self, inputs):
        self.state.data_to_send = inputs[self.inport]
        self.state.next_reading_time = self.timeLast + self.data_interval
        return self.state

    def outputFnc(self):
        sent_data = self.state.data_to_send
        self.state.data_to_send = None
        print(f"Water Quality Sensor simulated sending: {sent_data}")
        return {self.outport: sent_data}

    def intTransition(self):
        self.timeLast = self.state.next_reading_time  # Update timeLast
        self.state.next_reading_time = INFINITY
        return self.state