from pypdevs.simulator import Simulator
from model import WaterQualityModel

if __name__ == '__main__':
    model = WaterQualityModel()
    sim = Simulator(model)
    sim.setClassicDEVS()
    sim.setVerbose()  
    sim.setTerminationTime(60)  
    sim.simulate()