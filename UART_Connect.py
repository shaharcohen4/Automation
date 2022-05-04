import serial


class UARTconnection:

    def __init__(self, COM):
        self.com = COM

    def connectUART(self):
        connection = serial.Serial(port=self.com, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=None,
                                   xonxoff=0)
        return connection
