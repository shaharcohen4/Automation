import pyvisa as visa
import time




class powersupply:
    def __init__(self):
        self.rm = visa.ResourceManager()
        self.powersupply = self.rm.open_resource('USB0::0x2A8D::0x3402::MY61001083::0::INSTR')

    def output_state_powersupply(self, state, channel):
        self.powersupply.write(':OUTPut:STATe %d,(%s)' % (state, '@' + str(channel)))
        self.powersupply.write(':SOURce:VOLTage:SENSe:SOURce %s,(%s)' % ('EXTernal',  '@' + str(channel)))    # sense!!!

    def set_dc_voltage_powersupply(self, voltage, channel):
        self.powersupply.write(':SOURce:VOLTage:LEVel:IMMediate:AMPLitude %G,(%s)' % (voltage, '@' + str(channel)))

    def set_dc_current_powersupply(self, current, channel):
        self.powersupply.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G,(%s)' % (current, '@' + str(channel)))

    def get_dc_voltage_powersupply(self, channel):
        temp_values = self.powersupply.query_ascii_values(':MEASure:SCALar:VOLTage:DC? %s' % ('CH' + str(channel)))
        dc_v = temp_values[0]
        return dc_v

    def get_dc_current_powersupply(self, channel):
        temp_values = self.powersupply.query_ascii_values(':MEASure:SCALar:CURRent:DC? %s' % ('CH' + str(channel)))
        dc_c = temp_values[0]
        return dc_c


# a = powersupply()
# a.output_state_powersupply(1, 1)
# time.sleep(5)
# a.output_state_powersupply(0, 1)
# time.sleep(5)
# a.output_state_powersupply(1, 1)