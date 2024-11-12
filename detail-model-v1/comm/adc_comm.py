from pypdevs.DEVS import AtomicDEVS

class ADC(AtomicDEVS):
    def __init__(self, name):
        super().__init__(name)
        self.inport_ph = self.addInPort("in_ph")
        self.inport_tds = self.addInPort("in_tds")
        self.outport = self.addOutPort("out_adc")
        self.data = {}

    def extTransition(self, inputs):
        if self.inport_ph in inputs:
            self.data['ph'] = inputs[self.inport_ph]
        if self.inport_tds in inputs:
            self.data['tds'] = inputs[self.inport_tds]
        return self

    def outputFnc(self):
        return {self.outport: self.data}
