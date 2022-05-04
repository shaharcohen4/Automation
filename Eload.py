import pyvisa as visa
import time


class Eload:
    def __init__(self):
        self.rm = visa.ResourceManager()
        self.eload = self.rm.open_resource('USB0::0x2A8D::0x3802::MY60260413::0::INSTR')

    def output_state_eload(self, state, channel):
        self.eload.write(':OUTPut:STATe %d,(%s)' % (state, '@' + str(channel)))
        self.eload.write(':SOURce:VOLTage:SENSe:SOURce %s,(%s)' % ('EXTernal', '@' + str(channel)))  # sense!!!

    def set_cc_mode_eload(self, current, channel):
        self.eload.write(':CHANnel:LOAD %G' % (channel))
        self.eload.write(':SOURce:MODE %s' % ('CURR'))
        self.eload.write(':SOURce:CURRent:LEVel:IMMediate:AMPLitude %G,(%s)' % (current, '@' + str(channel)))

    def set_cv_mode_eload(self, voltage, channel):
        self.eload.write(':CHANnel:LOAD %G' % (channel))
        self.eload.write(':SOURce:MODE %s' % 'VOLT')
        self.eload.write(':SOURce:voltage:LEVel:IMMediate:AMPLitude %G,(%s)' % (voltage, '@' + str(channel)))

    def set_cr_mode_eload(self, resistance, channel):
        self.eload.write(':CHANnel:LOAD %G' % (channel))
        self.eload.write(':SOURce:MODE %s' % ('RES'))
        self.eload.write(':SOURce:RESistance:LEVel:IMMediate:AMPLitude %G,(%s)' % (resistance, '@' + str(channel)))

    def set_cp_mode_eload(self, power, channel):
        self.eload.write(':CHANnel:LOAD %G' % (channel))
        self.eload.write(':SOURce:MODE %s' % ('POWER'))
        self.eload.write(':SOURce:power:LEVel:IMMediate:AMPLitude %G,(%s)' % (power, '@' + str(channel)))


    def get_dc_curren_eload(self, channel):
        self.eload.write(':CHANnel:LOAD %G' % (channel))
        temp_values = self.eload.query_ascii_values(':MEASure:SCALar:CURRent:DC?')
        dc_current = temp_values[0]
        return dc_current

    def get_power_eload(self, channel):
        self.eload.write(':CHANnel:LOAD %G' % (channel))
        temp_values = self.eload.query_ascii_values(':MEASure:SCALar:POWer:DC?')
        power = temp_values[0]
        return power

    def get_dc_voltage_eload(self, channel):
        self.eload.write(':CHANnel:LOAD %G' % (channel))
        temp_values = self.eload.query_ascii_values(':MEASure:SCALar:VOLTage:DC?')
        voltage = temp_values[0]
        return voltage


# eload1 = Eload()
# eload1.output_state_eload(1,1)
# time.sleep(2)
# eload1.set_cv_mode_eload(4, 2)

