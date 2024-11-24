from pypdevs.DEVS import CoupledDEVS

from nodes.water_quality_node import WaterQualityNode
from nodes.water_level_node import WaterLevelNode
from nodes.water_quantity_node import WaterQuantityTypeOne

from sensors.ph_sensor import PHSensor
from sensors.temp_sensor import TempSensor
from sensors.tds_sensor import TDSSensor
from sensors.ultrasonic_sensor import UltrasonicSensor
from sensors.pulse_sensor import PulseSensor

from communications.adc_comm import ADC
from communications.spi_comm import SPI
from communications.uart_comm import UART
from communications.gpio_comm import GPIO

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

class WaterQuantityTypeOneModel(CoupledDEVS):
    def __init__(self):
        super().__init__("WaterQuantityTypeOneModel")
        print("Model Loaded")

        # Initialize sensors
        print("Initializing Sensors")
        pulse_sensor = self.addSubModel(PulseSensor("PulseSensor"))

        # Initialize communication models
        print("Initializing Communication Models")
        gpio_comm = self.addSubModel(GPIO("GPIO", data_types=["pulse"]))

        # Initialize water quantity node
        print("Initializing Water Quantity Node")
        water_quantity_node = self.addSubModel(WaterQuantityTypeOne("WaterQuantityNode"))

        # Initialize OneM2M interface
        print("Initializing OneM2M Interface")
        onem2m_interface = self.addSubModel(OneM2MInterface("OneM2MInterface"))

        # Initialize sink
        print("Initializing Sink")
        sink = self.addSubModel(Sink("Sink"))

        # Connect sensors to communication models
        print("Connecting Pulse Sensor to GPIO")
        self.connectPorts(pulse_sensor.out_port, gpio_comm.inports["pulse"])

        # Connect communication models to water quantity node
        print("Connecting GPIO output to Water Quantity Node GPIO input")
        self.connectPorts(gpio_comm.out_port, water_quantity_node.gpio_inport)


        # Connect water quantity node to OneM2M interface
        print("Connecting Water Quantity Node's out_port to OneM2M Interface's inport")
        self.connectPorts(water_quantity_node.out_port, onem2m_interface.inport)

        # Connect OneM2M interface to sink
        print("Connecting OneM2M Interface's out_port to Sink's inport")
        self.connectPorts(onem2m_interface.out_port, sink.inport)

        print("Model initialization complete")
        
        
        