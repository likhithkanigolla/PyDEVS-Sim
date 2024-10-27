from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY

class SensorState(object):
    def __init__(self):
        self.measurement = float("-inf")
        self.timestamp = float("-inf")

    def __str__(self):
        return f"SensorState(measurement={self.measurement}, timestamp={self.timestamp})"


class Sensor(AtomicDEVS):
    def __init__(self):
        AtomicDEVS.__init__(self, "Sensor")
        self.state = SensorState()
        self.processing_time = 1.0
        self.inport = self.addInPort("input")
        self.outport = self.addOutPort("output")
        print(f"Initialized Sensor with state: {self.state}")

    def timeAdvance(self):
        if self.state is None:
            print("timeAdvance called: returning INFINITY")
            return INFINITY
        else:
            print(f"timeAdvance called: returning {self.processing_time}")
            return self.processing_time

    def outputFnc(self):
        print(f"outputFnc called: outputting {self.state}")
        return {self.outport: {self.state}}

    def extTransition(self, inputs):
        print(f"extTransition called with inputs: {inputs}")
        self.state.timestamp = list(inputs[self.inport])[0]
        self.state.measurement = list(inputs[self.inport])[1]
        print(f"State updated to: {self.state}")
        return self.state

    def intTransition(self):
        print(f"intTransition called: current state is {self.state}")
        return self.state
