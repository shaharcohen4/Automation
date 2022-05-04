import pyvisa as visa
import time


class DMM:
    def __init__(self):
        self.rm = visa.ResourceManager()
        self.dmm = self.rm.open_resource('USB0::0x2A8D::0x0101::MY60033224::0::INSTR')

    def get_dc_current_dmm(self):
        temp_values = self.dmm.query_ascii_values(':MEASure:CURRent:DC?')
        dccurrent = temp_values[0]
        return dccurrent

    def get_ac_current_dmm(self):
        temp_values = self.dmm.query_ascii_values(':MEASure:CURRent:AC?')
        accurrent = temp_values[0]
        return accurrent

    def get_ac_voltage_dmm(self):
        temp_values = self.dmm.query_ascii_values(':MEASure:VOLTage:AC?')
        acvoltage = temp_values[0]
        return acvoltage

    def get_dc_voltage_dmm(self):
        temp_values = self.dmm.query_ascii_values(':MEASure:VOLTage:DC?')
        dcvoltage = temp_values[0]
        return dcvoltage

    def get_temperature_dmm(self):
        temp_values = self.dmm.query_ascii_values(':MEASure:TEMPerature? %s,%s' % ('TCouple', 'K'))
        temperature = temp_values[0]
        return temperature

    def get_capacitance_dmm(self):
        temp_values = self.dmm.query_ascii_values(':MEASure:CAPacitance?')
        capacitance = temp_values[0]
        return capacitance

    def get_resistance_dmm(self):
        temp_values = self.dmm.query_ascii_values(':MEASure:FRESistance?')
        fresistance = temp_values[0]
        return fresistance
