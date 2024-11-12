from pypdevs.DEVS import AtomicDEVS

class SPI(AtomicDEVS):
    def __init__(self, name):
        super().__init__(name)
        self.inport_temp = self.addInPort("in_temp")
        self.outport = self.addOutPort("out_spi")
        self.data = {}

    def extTransition(self, inputs):
        if self.inport_temp in inputs:
            self.data['temp'] = inputs[self.inport_temp]
        return self

    def outputFnc(self):
        return {self.outport: self.data}
