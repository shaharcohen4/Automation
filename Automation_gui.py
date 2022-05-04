from ReadFromExcel import ReadFromExcelFile
from PyQt6 import QtCore, QtGui, QtWidgets
from Efficiency import Efficiency



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(792, 577)
        font = QtGui.QFont()
        font.setPointSize(26)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(250, 10, 301, 111))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(540, 260, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")


        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(340, 460, 81, 51))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.run_test)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(540, 200, 121, 41))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(50, 110, 131, 61))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(60, 372, 521, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.checkBox1 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox1.setGeometry(QtCore.QRect(20, 190, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox1.setFont(font)
        self.checkBox1.setObjectName("checkBox1")
        self.checkBox2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox2.setGeometry(QtCore.QRect(20, 220, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox2.setFont(font)
        self.checkBox2.setObjectName("checkBox2")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 792, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Automation"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Efficiency\n"""))
        self.comboBox.setItemText(1, _translate("MainWindow", "Tx I_dc maserment"))
        self.pushButton.setText(_translate("MainWindow", "run"))
        self.label_2.setText(_translate("MainWindow", "Test:"))
        self.label_3.setText(_translate("MainWindow", "Project:"))
        self.checkBox1.setText(_translate("MainWindow", "MDR"))
        self.checkBox2.setText(_translate("MainWindow", "Mytronix B400"))
        self.label_4.setText(_translate("MainWindow", ""))



    def run_test(self):
#         chack the name of project
# -----------------------------------------------------------------------------------------------------------------------
        checkbox_project = [self.checkBox1, self.checkBox2]
        counter = 0
        project_number = 0
        for i in checkbox_project:
            if i.isChecked() == bool(True):
                counter += 1
                choosen_project = project_number
            project_number += 1

        if counter == 0:
            self.label_4.setText("Error : Project was not selected!")
        elif counter > 1:
            self.label_4.setText("Error : You have been selected 2 or more project")
        else:
            self.label_4.setText("You have been selcted "+ checkbox_project[choosen_project].text() + " project")
            print(checkbox_project[choosen_project].text())
            file = ReadFromExcelFile(checkbox_project[choosen_project].text())
            parameters = file.Getparams()
            print(parameters)
            test = eval(str(self.comboBox.currentText()))(parameters)
            test.run()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
