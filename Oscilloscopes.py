import pyvisa as visa
import time

class Oscilloscopes :
    def __init__(self):
        self.rm = visa.ResourceManager()
        self.Oscilloscopes = self.rm.open_resource('USB0::0x0957::0x17A8::MY52101229::0::INSTR')

    def get_voltage_avarge(self):

        temp_values = self.Oscilloscopes.query_ascii_values(':MEASure:VAVerage? %s,%s' % ('DISPlay', 'CHANNEL1'))
        value = temp_values[0]
        return value

# my_ossiliscope = Oscilloscopes()
# print(my_ossiliscope.get_voltage_avarge())