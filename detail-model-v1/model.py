from pypdevs.DEVS import CoupledDEVS

# Import key components
from nodes.water_quality_sensor import WaterQualityNode
from components.onem2m_interface import OneM2MInterface
from sink import Sink

# Individual sensors
from sensors.ph_sensor import PHSensor
from sensors.temp_sensor import TempSensor
from sensors.tds_sensor import TDSSensor

# Communication models
from communications.adc_comm import ADC
from communications.spi_comm import SPI

class WaterQualityModel(CoupledDEVS):
    def __init__(self):
        super().__init__("WaterQualityModel")
        print("Model Loaded")

        # Initialize sensors
        print("Initializing Sensors")
        ph_sensor = self.addSubModel(PHSensor("PHSensor"))
        temp_sensor = self.addSubModel(TempSensor("TempSensor"))
        tds_sensor = self.addSubModel(TDSSensor("TDSSensor"))

        # Initialize communication models
        print("Initializing Communication Models")
        adc = self.addSubModel(ADC("ADC"))
        spi = self.addSubModel(SPI("SPI"))

        # Initialize water quality node
        print("Initializing Water Quality Node")
        water_quality_node = self.addSubModel(WaterQualityNode("WM-WD-KH98-00"))

        # Initialize OneM2M interface
        print("Initializing OneM2M Interface")
        onem2m_interface = self.addSubModel(OneM2MInterface("OneM2MInterface"))

        # Initialize sink
        print("Initializing Sink")
        sink = self.addSubModel(Sink("Sink"))

        # Connect sensors to communication models
        print("Connecting PH Sensor to ADC")
        self.connectPorts(ph_sensor.outport, adc.inport_ph)
        print("Connecting TDS Sensor to ADC")
        self.connectPorts(tds_sensor.outport, adc.inport_tds)
        print("Connecting Temperature Sensor to SPI")
        self.connectPorts(temp_sensor.outport, spi.inport_temp)

        # Connect communication models to water quality node
        print("Connecting ADC output to Water Quality Node ADC input")
        self.connectPorts(adc.outport, water_quality_node.adc_inport)
        print("Connecting SPI output to Water Quality Node SPI input")
        self.connectPorts(spi.outport, water_quality_node.spi_inport)

        # Connect water quality node to OneM2M interface
        print("Connecting Water Quality Node's outport to OneM2M Interface's inport")
        self.connectPorts(water_quality_node.outport, onem2m_interface.inport)

        # Connect OneM2M interface to sink
        print("Connecting OneM2M Interface's outport to Sink's inport")
        self.connectPorts(onem2m_interface.outport, sink.inport)

        print("Model initialization complete")
        