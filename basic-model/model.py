from pypdevs.DEVS import CoupledDEVS

from water_quality_sensor import WaterQualitySensor
from onem2m_interface import OneM2MInterface
from sink import Sink

class WaterQualityModel(CoupledDEVS):
    def __init__(self):
        CoupledDEVS.__init__(self, "WaterQualityModel")

        self.sensor = self.addSubModel(WaterQualitySensor("Sensor_01", data_interval=10))
        self.onem2m = self.addSubModel(OneM2MInterface(simulated_delay=2))  
        self.sink = self.addSubModel(Sink())

        self.connectPorts(self.sensor.outport, self.onem2m.inport)
        self.connectPorts(self.onem2m.outport, self.sink.inport)