import pandas as pd
import openpyxl


class ReadFromExcelFile:

    def __init__(self, projectname):
        self.data = pd.read_excel(r"C:\Users\scohen\PycharmProjects\Automation\parameters.xlsx", sheet_name='Sheet1')
        self.projectname = projectname
        self.params = self.Getparams()

    def Getparams(self):
        params = {}
        for i in range(len(self.data)):
            params.__setitem__(self.data._get_value(i, 'Parameters'), self.data._get_value(i, self.projectname))

        return params





# file = ReadFromExcelFile('MDR')
# parameters = file.Getparams()
# print(parameters)