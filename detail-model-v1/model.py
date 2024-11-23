from pypdevs.DEVS import CoupledDEVS
from nodes.water_quality_node import WaterQualityNode
from nodes.water_level_node import WaterLevelNode
from components.onem2m_interface import OneM2MInterface
from sink import Sink
from sensors.ph_sensor import PHSensor
from sensors.temp_sensor import TempSensor
from sensors.tds_sensor import TDSSensor
from sensors.ultrasonic_sensor import UltrasonicSensor
from communications.adc_comm import ADC
from communications.spi_comm import SPI

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
        adc_level = self.addSubModel(ADC("ADC_WaterLevel", data_types=["distance"]))
        spi = self.addSubModel(SPI("SPI"))

        # Nodes
        water_quality_node = self.addSubModel(WaterQualityNode("WaterQualityNode"))
        water_level_node = self.addSubModel(WaterLevelNode("WaterLevelNode"))

        # Interfaces and Sink
        onem2m_interface = self.addSubModel(OneM2MInterface("OneM2MInterface"))
        sink = self.addSubModel(Sink("Sink"))

        # Connect sensors to communication models
        self.connectPorts(ph_sensor.outport, adc_quality.inports["pH"])
        self.connectPorts(tds_sensor.outport, adc_quality.inports["TDS"])
        self.connectPorts(temp_sensor.outport, spi.inport_temp)
        # self.connectPorts(ultrasonic_sensor.outport, adc_level.inports["distance"])

        # Connect communication models to nodes
        self.connectPorts(adc_quality.outport, water_quality_node.adc_inport)
        self.connectPorts(spi.outport, water_quality_node.spi_inport)
        self.connectPorts(adc_level.outport, water_level_node.adc_inport)

        # Connect nodes to the OneM2M interface
        self.connectPorts(water_quality_node.outport, onem2m_interface.inport)
        self.connectPorts(water_level_node.outport, onem2m_interface.inport)

        # Connect OneM2M interface to sink
        self.connectPorts(onem2m_interface.outport, sink.inport)


class WaterLevelModel(CoupledDEVS):
    def __init__(self):
        super().__init__("WaterLevelModel")
        print("Model Loaded")

        # Initialize sensors
        print("Initializing Sensors")
        ultrasonic_sensor = self.addSubModel(UltrasonicSensor("UltrasonicSensor"))

        # Initialize communication models
        print("Initializing Communication Models")
        adc_level = self.addSubModel(ADC("ADC_WaterLevel", data_types=["distance"]))

        # Initialize water level node
        print("Initializing Water Level Node")
        water_level_node = self.addSubModel(WaterLevelNode("WaterLevelNode"))

        # Initialize OneM2M interface
        print("Initializing OneM2M Interface")
        onem2m_interface = self.addSubModel(OneM2MInterface("OneM2MInterface"))

        # Initialize sink
        print("Initializing Sink")
        sink = self.addSubModel(Sink("Sink"))

        # Connect sensors to communication models
        print("Connecting Ultrasonic Sensor to ADC")
        self.connectPorts(ultrasonic_sensor.outport, adc_level.inports["distance"])

        # Connect communication models to water level node
        print("Connecting ADC output to Water Level Node ADC input")
        self.connectPorts(adc_level.outport, water_level_node.adc_inport)

        # Connect water level node to OneM2M interface
        print("Connecting Water Level Node's outport to OneM2M Interface's inport")
        self.connectPorts(water_level_node.outport, onem2m_interface.inport)

        # Connect OneM2M interface to sink
        print("Connecting OneM2M Interface's outport to Sink's inport")
        self.connectPorts(onem2m_interface.outport, sink.inport)

        print("Model initialization complete")