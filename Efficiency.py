from Eload import Eload
from Power_supply import powersupply
from Digit_multimeter import DMM
from ReadFromExcel import ReadFromExcelFile
from UART_Connect import UARTconnection
from Robot import Robot
import time
import numpy as np


class Efficiency:

    def __init__(self, parameters):
        self.robot = Robot()
        self.dmm = DMM()
        self.powersupply = powersupply()
        self.eload = Eload()
        self.parameters = parameters
        self.efficiency_parameters = self.getefficiencyparameters()
        # self.TxUART = UARTconnection('COM9')
        self.numberofpositions = None
        self.vouts = []
        self.voutscurrents = []
        self.vins = []
        self.vinscurrents = []
        self.FinalTxvoltages = None
        self.FinalTxcurrents = None
        self.FinalRxvoltages = None
        self.FinalRxcurrents = None
        self.Finalefficiency = None
        self.counter = None
        self.listofvalues = None
        self.efficiency = None
        self.position = None
        self.z_positions = None
        self.y_positions = None

    def run(self):
        print(self.parameters['Min Eload value'], self.parameters['Max Eload value'], self.parameters['Number of steps'])
        self.listofvalues = list(np.arange(self.parameters['Min Eload value'], self.parameters['Max Eload value'],
                                           self.parameters['Number of steps']))
        print(self.listofvalues)
        self.counter = len(self.listofvalues)
        self.position = isinstance(self.numberofpositions, int)
        self.FinalTxvoltages = np.array(list(range(self.counter)), ndmin=2)
        self.FinalTxcurrents = np.array(list(range(self.counter)), ndmin=2)
        self.FinalRxvoltages = np.array(list(range(self.counter)), ndmin=2)
        self.FinalRxcurrents = np.array(list(range(self.counter)), ndmin=2)
        self.Finalefficiency = np.array(list(range(self.counter)), ndmin=2)
        robot_start_positions = self.robot.get_current_position()
        self.y_positions = list(np.arange(self.parameters['Min xy position'], self.parameters['Max xy position'],
                                          self.parameters['Step size']))
        self.z_positions = list(np.arange(self.parameters['Min z position'], self.parameters['Max z position'],
                                          self.parameters['Step size']))
        self.numberofpositions = len(self.z_positions) * len(self.y_positions)
        run = True
        if self.parameters['Mode'] == 'CC':
            while run:
                for i in self.z_positions:
                    for j in self.y_positions:
                        self.robot.set_position(robot_start_positions, 0, j, i)
                        self.powersupply.set_dc_voltage_powersupply(self.parameters['Input voltage'], 1)
                        self.powersupply.set_dc_current_powersupply(self.parameters['Input current'], 1)
                        time.sleep(1)
                        self.powersupply.output_state_powersupply(1, 1)
                        time.sleep(1)
                        # self.Txcommand(1)
                        time.sleep(5)
                        self.Eloadcurrent()
                        self.powersupply.output_state_powersupply(0, 1)
                        self.numberofpositions = self.numberofpositions - 1
                if self.numberofpositions == 0:
                    self.position = False

        if self.parameters['Mode'] == 'CV':
            while self.position:
                for i in self.z_positions:
                    for j in self.y_positions:
                        self.robot.set_position(robot_start_positions, 0, j, i)
                        self.powersupply.set_dc_voltage_powersupply(self.parameters['Input voltage'], 1)
                        self.powersupply.set_dc_current_powersupply(self.parameters['Input current'], 1)
                        time.sleep(1)
                        self.powersupply.output_state_powersupply(1, 1)
                        time.sleep(1)
                        # self.Txcommand(1)
                        time.sleep(5)
                        self.Eloadvoltage()
                        self.powersupply.output_state_powersupply(0, 1)
                        self.numberofpositions = self.numberofpositions - 1
                if self.numberofpositions == 0:
                    self.position = False

        return self.efficiency

    def Eloadvoltage(self):
        for i in range(self.counter):
            self.eload.set_cv_mode_eload(self.listofvalues[i], 1)
            self.eload.output_state_eload(1, 1)
            time.sleep(1)
            Txvoltage, Txcurrent, Rxvoltage, Rxcurrent = self.measurments()
            self.vouts.append(Rxvoltage)
            self.vins.append(Txvoltage)
            self.vinscurrents.append(Txcurrent)
            self.voutscurrents.append(Rxcurrent)
            time.sleep(2)
        self.Efficiencycalc()
        self.concatenate()
        self.Clearfunction()
        self.eload.output_state_eload(0, 1)

    def Eloadcurrent(self):
        for i in range(self.counter):
            print(self.listofvalues[i])
            self.eload.set_cc_mode_eload(self.listofvalues[i], 1)
            self.eload.output_state_eload(1, 1)
            time.sleep(1)
            Txvoltage, Txcurrent, Rxvoltage, Rxcurrent = self.measurments()
            self.vouts.append(Rxvoltage)
            self.vins.append(Txvoltage)
            self.vinscurrents.append(Txcurrent)
            self.voutscurrents.append(Rxcurrent)
            time.sleep(2)
        self.Efficiencycalc()
        self.concatenate()
        self.Clearfunction()
        self.eload.output_state_eload(0, 1)

    def measurments(self):
        Txvoltage = float(self.powersupply.get_dc_voltage_powersupply(1))
        Txcurrent = float(self.powersupply.get_dc_current_powersupply(1))
        Rxvoltage = float(self.dmm.get_dc_voltage_dmm())
        Rxcurrent = float(self.eload.get_dc_curren_eload(1))
        return Txvoltage, Txcurrent, Rxvoltage, Rxcurrent

    def Efficiencycalc(self):
        powerin = np.array(self.vins) * np.array(self.vinscurrents)
        powerout = np.array(self.vouts) * np.array(self.voutscurrents)
        self.efficiency = powerout / powerin * 100

    def getefficiencyparameters(self):
        parameters_list = ['Mode', 'Max Eload value', 'Min Eload value', 'Number of steps', 'Input voltage',
                           'Input current', 'Step size', 'Max z position', 'Min z position', 'Max xy position',
                           'Min xy position']
        efficiency_parameters = {}
        for i in parameters_list:
            efficiency_parameters.__setitem__(i, self.parameters[i])
        return efficiency_parameters

    def Clearfunction(self):
        self.vouts.clear()
        self.voutscurrents.clear()
        self.vins.clear()
        self.vinscurrents.clear()

    def concatenate(self):
        self.FinalTxvoltages = np.concatenate((self.FinalTxvoltages, np.array(self.vins, ndmin=2)), axis=0)
        self.FinalTxcurrents = np.concatenate((self.FinalTxcurrents, np.array(self.vinscurrents, ndmin=2)), axis=0)
        self.FinalRxvoltages = np.concatenate((self.FinalRxvoltages, np.array(self.vouts, ndmin=2)), axis=0)
        self.FinalRxcurrents = np.concatenate((self.FinalRxcurrents, np.array(self.voutscurrents, ndmin=2)), axis=0)
        self.Finalefficiency = np.concatenate((self.Finalefficiency, np.array(self.efficiency, ndmin=2)), axis=0)

    # def Txcommand(self, StartorStop):
    #     if StartorStop == 1:
    #         self.TxUART.write(bytes.fromhex('01'))
    #         self.TxUART.write(bytes.fromhex('06'))
    #         self.TxUART.write(bytes.fromhex('00'))
    #         self.TxUART.write(bytes.fromhex('05'))
    #         self.TxUART.write(bytes.fromhex('00'))
    #         self.TxUART.write(bytes.fromhex('00'))
    #         self.TxUART.write(bytes.fromhex('99'))
    #         self.TxUART.write(bytes.fromhex('CB'))
    #     if StartorStop == 0:
    #         self.TxUART.write(bytes.fromhex('01'))
    #         self.TxUART.write(bytes.fromhex('06'))
    #         self.TxUART.write(bytes.fromhex('00'))
    #         self.TxUART.write(bytes.fromhex('05'))
    #         self.TxUART.write(bytes.fromhex('00'))
    #         self.TxUART.write(bytes.fromhex('01'))
    #         self.TxUART.write(bytes.fromhex('58'))
    #         self.TxUART.write(bytes.fromhex('0B'))


# file = ReadFromExcelFile('MDR')
# parameters = file.Getparams()
# test = Efficiency(parameters)
# print(parameters)
# test.run()
