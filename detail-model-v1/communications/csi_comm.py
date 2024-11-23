from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY

class CSIComm(AtomicDEVS):
    def __init__(self, name, csi):
        AtomicDEVS.__init__(self, name)
        self.state = "idle"
        self.csi = csi
        self.input_ports = ["in"]
        self.output_ports = ["out"]
        self.current_packet = None
        self.packet_queue = []

    def intTransition(self):
        if self.state == "idle" and len(self.packet_queue) > 0:
            self.current_packet = self.packet_queue.pop(0)
            self.state = "transmitting"
        elif self.state == "transmitting":
            self.state = "idle"
        return self.state

    def extTransition(self, inputs):
        if self.state == "idle" and len(inputs["in"]) > 0:
            self.packet_queue.append(inputs["in"][0])
        return self.state

    def outputFnc(self):
        if self.state == "transmitting":
            return {"out": [self.current_packet]}
        return {}