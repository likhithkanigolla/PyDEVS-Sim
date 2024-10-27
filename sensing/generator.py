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
        print(f"Initialized Generator with {num_to_generate} items to generate.")

    def timeAdvance(self):
        print(f"Time advance called. Time until next event: {self.state.time_until_next}")
        return self.state.time_until_next

    def outputFnc(self):
        output = {self.outport: {self.state.current_time, self.state.num_to_generate}}
        print(f"Output function called. Output: {output}")
        return output

    def intTransition(self):
        self.state.current_time += self.timeAdvance()
        print(f"Internal transition called. Current time: {self.state.current_time}")
        if self.state.num_to_generate == 0:
            self.state.time_until_next = float("inf")
            print("No more items to generate. Setting time until next to infinity.")
        else:
            self.state.time_until_next = random.expovariate(100)
            self.state.num_to_generate -= 1
            print(f"Generated new item. Items left: {self.state.num_to_generate}. Time until next: {self.state.time_until_next}")

        return self.state
