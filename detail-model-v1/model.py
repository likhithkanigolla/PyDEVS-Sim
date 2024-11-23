from pypdevs.DEVS import CoupledDEVS

from nodes.water_quality_node import WaterQualityNode
from nodes.water_level_node import WaterLevelNode


from sensors.ph_sensor import PHSensor
from sensors.temp_sensor import TempSensor
from sensors.tds_sensor import TDSSensor
from sensors.ultrasonic_sensor import UltrasonicSensor

from communications.adc_comm import ADC
from communications.spi_comm import SPI
from communications.uart_comm import UART

from components.onem2m_interface import OneM2MInterface
from sink import Sink

class WaterQualityModel(CoupledDEVS):
    def __init__(self):
        super().__init__("WaterQualityModel")

        # Sensors
        ph_sensor = self.addSubModel(PHSensor("PHSensor"))
        temp_sensor = self.addSubModel(TempSensor("TempSensor"))
        tds_sensor = self.addSubModel(TDSSensor("TDSSensor"))
        # ultrasonic_sensor = self.addSubModel(UltrasonicSensor("UltrasonicSensor"))

        # Communication models
        adc_quality = self.addSubModel(ADC("ADC_WaterQuality", data_types=["pH", "TDS"]))
        spi_quality = self.addSubModel(SPI("SPI", data_types=["temperature"]))

        # Nodes
        water_quality_node = self.addSubModel(WaterQualityNode("WaterQualityNode"))
        water_level_node = self.addSubModel(WaterLevelNode("WaterLevelNode"))

        # Interfaces and Sink
        onem2m_interface = self.addSubModel(OneM2MInterface("OneM2MInterface"))
        sink = self.addSubModel(Sink("Sink"))

        # Connect sensors to communication models
        self.connectPorts(ph_sensor.out_port, adc_quality.inports["pH"])
        self.connectPorts(tds_sensor.out_port, adc_quality.inports["TDS"])
        self.connectPorts(temp_sensor.out_port, spi_quality.inports["temperature"])
        # self.connectPorts(ultrasonic_sensor.out_port, adc_level.inports["distance"])

        # Connect communication models to nodes
        self.connectPorts(adc_quality.out_port, water_quality_node.adc_inport)
        self.connectPorts(spi_quality.out_port, water_quality_node.spi_inport)

        # Connect nodes to the OneM2M interface
        self.connectPorts(water_quality_node.out_port, onem2m_interface.inport)
        self.connectPorts(water_level_node.out_port, onem2m_interface.inport)

        # Connect OneM2M interface to sink
        self.connectPorts(onem2m_interface.out_port, sink.inport)

class WaterLevelModel(CoupledDEVS):
    def __init__(self, name=None):
        super().__init__("WaterLevelModel")
        
        # Sensors
        ultrasonic_sensor = self.addSubModel(UltrasonicSensor("UltrasonicSensor"))
        temp_sensor = self.addSubModel(TempSensor("TempSensor"))
        
        # Communication models
        uart_level = self.addSubModel(UART("UART", data_types=["distance"]))
        spi_level = self.addSubModel(SPI("SPI", data_types=["temperature"]))
        
        # Nodes
        water_level_node = self.addSubModel(WaterLevelNode("WaterLevelNode"))
        
        # Interfaces and Sink
        onem2m_interface = self.addSubModel(OneM2MInterface("OneM2MInterface"))
        sink = self.addSubModel(Sink("Sink"))
        
        # Connect sensors to communication models
        self.connectPorts(ultrasonic_sensor.out_port, uart_level.inports["distance"])
        self.connectPorts(temp_sensor.out_port, spi_level.inports["temperature"])
        
        # Connect communication models to nodes
        self.connectPorts(uart_level.out_port, water_level_node.uart_inport)
        self.connectPorts(spi_level.out_port, water_level_node.spi_inport)
    
        # Connect nodes to the OneM2M interface
        self.connectPorts(water_level_node.out_port, onem2m_interface.inport)
        
        # Connect OneM2M interface to sink
        self.connectPorts(onem2m_interface.out_port, sink.inport)

        
        