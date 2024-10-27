from pypdevs.simulator import Simulator

from model import Model


if __name__ == '__main__':
    values = []
    num_to_generate = 10

    model = Model(num_to_generate)
    sim = Simulator(model)
    sim.setClassicDEVS()
    sim.setVerbose()
    sim.setTerminationTime(5)
    sim.simulate()


