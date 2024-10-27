from pypdevs.DEVS import AtomicDEVS

import random


class GeneratorState(object):
    def __init__(self, num_to_generate):
        self.current_time = 0.0
        self.time_until_next = 0.0
        self.num_to_generate = num_to_generate


class Generator(AtomicDEVS):
    def __init__(self, num_to_generate = 5):
        AtomicDEVS.__init__(self, "Generator")
        self.state = GeneratorState(num_to_generate)
        self.outport = self.addOutPort("output")


    def timeAdvance(self):
        return self.state.time_until_next


    def outputFnc(self):
        return {self.outport: { self.state.current_time, self.state.num_to_generate } }


    def intTransition(self):
        self.state.current_time += self.timeAdvance()
        if self.state.num_to_generate == 0:
            self.state.time_until_next = float("inf")
        else:
            self.state.time_until_next = random.expovariate(100)
            self.state.num_to_generate -= 1

        return self.state
