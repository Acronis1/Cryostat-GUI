# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ITC_control.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ITCcontrol(object):
    def setupUi(self, ITCcontrol):
        ITCcontrol.setObjectName("ITCcontrol")
        ITCcontrol.resize(535, 391)
        self.centralwidget = QtWidgets.QWidget(ITCcontrol)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 20, 491, 331))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout.addWidget(self.spinBox, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.spinBox_2 = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        self.spinBox_2.setObjectName("spinBox_2")
        self.gridLayout.addWidget(self.spinBox_2, 1, 1, 1, 1)
        self.spinBox_3 = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        self.spinBox_3.setObjectName("spinBox_3")
        self.gridLayout.addWidget(self.spinBox_3, 2, 1, 1, 1)
        self.spinBox_6 = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        self.spinBox_6.setObjectName("spinBox_6")
        self.gridLayout.addWidget(self.spinBox_6, 5, 1, 1, 1)
        self.spinBox_4 = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        self.spinBox_4.setObjectName("spinBox_4")
        self.gridLayout.addWidget(self.spinBox_4, 3, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)
        self.comboBox_2 = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.gridLayout.addWidget(self.comboBox_2, 6, 1, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.comboBox, 4, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.line = QtWidgets.QFrame(self.horizontalLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.Needle = QtWidgets.QVBoxLayout()
        self.Needle.setObjectName("Needle")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_NeedleValve = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_NeedleValve.setObjectName("label_NeedleValve")
        self.horizontalLayout.addWidget(self.label_NeedleValve)
        self.Force_Needle_enable = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.Force_Needle_enable.setEnabled(False)
        self.Force_Needle_enable.setCheckable(True)
        self.Force_Needle_enable.setChecked(True)
        self.Force_Needle_enable.setObjectName("Force_Needle_enable")
        self.horizontalLayout.addWidget(self.Force_Needle_enable)
        self.Needle.addLayout(self.horizontalLayout)
        self.NeedleValve_bar = QtWidgets.QProgressBar(self.horizontalLayoutWidget)
        self.NeedleValve_bar.setEnabled(True)
        self.NeedleValve_bar.setProperty("value", 0)
        self.NeedleValve_bar.setObjectName("NeedleValve_bar")
        self.Needle.addWidget(self.NeedleValve_bar)
        self.Needle_slider = QtWidgets.QHBoxLayout()
        self.Needle_slider.setObjectName("Needle_slider")
        self.Slider_Needle = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.Slider_Needle.setEnabled(True)
        self.Slider_Needle.setMaximum(100)
        self.Slider_Needle.setOrientation(QtCore.Qt.Horizontal)
        self.Slider_Needle.setObjectName("Slider_Needle")
        self.Needle_slider.addWidget(self.Slider_Needle)
        spacerItem = QtWidgets.QSpacerItem(31, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.Needle_slider.addItem(spacerItem)
        self.Needle.addLayout(self.Needle_slider)
        self.Enable_NeedleValve = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.Enable_NeedleValve.setObjectName("Enable_NeedleValve")
        self.Needle.addWidget(self.Enable_NeedleValve)
        self.verticalLayout.addLayout(self.Needle)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.line_2 = QtWidgets.QFrame(self.horizontalLayoutWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_2.addWidget(self.line_2)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setHorizontalSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_8 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 1, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 4, 0, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_13.setObjectName("label_13")
        self.gridLayout_2.addWidget(self.label_13, 6, 0, 1, 1)
        self.lcdNumber = QtWidgets.QLCDNumber(self.horizontalLayoutWidget)
        self.lcdNumber.setObjectName("lcdNumber")
        self.gridLayout_2.addWidget(self.lcdNumber, 1, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_12.setObjectName("label_12")
        self.gridLayout_2.addWidget(self.label_12, 5, 0, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.horizontalLayoutWidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_2.addWidget(self.progressBar, 5, 1, 1, 1)
        self.lcdNumber_2 = QtWidgets.QLCDNumber(self.horizontalLayoutWidget)
        self.lcdNumber_2.setObjectName("lcdNumber_2")
        self.gridLayout_2.addWidget(self.lcdNumber_2, 2, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 3, 0, 1, 1)
        self.lcdNumber_3 = QtWidgets.QLCDNumber(self.horizontalLayoutWidget)
        self.lcdNumber_3.setObjectName("lcdNumber_3")
        self.gridLayout_2.addWidget(self.lcdNumber_3, 3, 1, 1, 1)
        self.lcdNumber_4 = QtWidgets.QLCDNumber(self.horizontalLayoutWidget)
        self.lcdNumber_4.setObjectName("lcdNumber_4")
        self.gridLayout_2.addWidget(self.lcdNumber_4, 4, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 2, 0, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_14.setObjectName("label_14")
        self.gridLayout_2.addWidget(self.label_14, 7, 0, 1, 1)
        self.lcdNumber_5 = QtWidgets.QLCDNumber(self.horizontalLayoutWidget)
        self.lcdNumber_5.setObjectName("lcdNumber_5")
        self.gridLayout_2.addWidget(self.lcdNumber_5, 6, 1, 1, 1)
        self.lcdNumber_8 = QtWidgets.QLCDNumber(self.horizontalLayoutWidget)
        self.lcdNumber_8.setObjectName("lcdNumber_8")
        self.gridLayout_2.addWidget(self.lcdNumber_8, 7, 1, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_15.setObjectName("label_15")
        self.gridLayout_2.addWidget(self.label_15, 8, 0, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_16.setObjectName("label_16")
        self.gridLayout_2.addWidget(self.label_16, 9, 0, 1, 1)
        self.lcdNumber_6 = QtWidgets.QLCDNumber(self.horizontalLayoutWidget)
        self.lcdNumber_6.setObjectName("lcdNumber_6")
        self.gridLayout_2.addWidget(self.lcdNumber_6, 9, 1, 1, 1)
        self.lcdNumber_7 = QtWidgets.QLCDNumber(self.horizontalLayoutWidget)
        self.lcdNumber_7.setObjectName("lcdNumber_7")
        self.gridLayout_2.addWidget(self.lcdNumber_7, 8, 1, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout_2)
        # ITCcontrol.setCentralWidget(self.centralwidget)
        # self.menubar = QtWidgets.QMenuBar(ITCcontrol)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 535, 21))
        # self.menubar.setObjectName("menubar")
        # ITCcontrol.setMenuBar(self.menubar)
        # self.statusbar = QtWidgets.QStatusBar(ITCcontrol)
        # self.statusbar.setObjectName("statusbar")
        # ITCcontrol.setStatusBar(self.statusbar)

        self.retranslateUi(ITCcontrol)
        # self.Enable_NeedleValve.clicked.connect(self.Slider_Needle.deleteLater)
        QtCore.QMetaObject.connectSlotsByName(ITCcontrol)

    def retranslateUi(self, ITCcontrol):
        _translate = QtCore.QCoreApplication.translate
        ITCcontrol.setWindowTitle(_translate("ITCcontrol", "MainWindow"))
        self.label_3.setText(_translate("ITCcontrol", "Int"))
        self.label_2.setText(_translate("ITCcontrol", "Prop"))
        self.label_4.setText(_translate("ITCcontrol", "Derivative"))
        self.label_5.setText(_translate("ITCcontrol", "Heater Output"))
        self.label_6.setText(_translate("ITCcontrol", "Heater Sensor"))
        self.comboBox_2.setItemText(0, _translate("ITCcontrol", "heater man, gas man"))
        self.comboBox_2.setItemText(1, _translate("ITCcontrol", "heater auto, gas man"))
        self.comboBox_2.setItemText(2, _translate("ITCcontrol", "heater man, gas auto"))
        self.comboBox_2.setItemText(3, _translate("ITCcontrol", "heater auto, gas auto"))
        self.comboBox.setItemText(0, _translate("ITCcontrol", "Sensor 1"))
        self.comboBox.setItemText(1, _translate("ITCcontrol", "Sensor 2"))
        self.comboBox.setItemText(2, _translate("ITCcontrol", "Sensor 3"))
        self.label_7.setText(_translate("ITCcontrol", "Autocontrol"))
        self.label.setText(_translate("ITCcontrol", "Set Temp"))
        self.label_NeedleValve.setText(_translate("ITCcontrol", "Gas Output"))
        self.Force_Needle_enable.setText(_translate("ITCcontrol", "Needle on manual"))
        self.Enable_NeedleValve.setText(_translate("ITCcontrol", "Force Needle Manual"))
        self.label_8.setText(_translate("ITCcontrol", "Temperature 1"))
        self.label_11.setText(_translate("ITCcontrol", "Temperature error"))
        self.label_13.setText(_translate("ITCcontrol", "Heater Output [V]"))
        self.label_12.setText(_translate("ITCcontrol", "Heater Output [%]"))
        self.label_10.setText(_translate("ITCcontrol", "Temperature 3"))
        self.label_9.setText(_translate("ITCcontrol", "Temperature 2"))
        self.label_14.setText(_translate("ITCcontrol", "Proportional band"))
        self.label_15.setText(_translate("ITCcontrol", "Integration action time"))
        self.label_16.setText(_translate("ITCcontrol", "Derivative action time"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ITCcontrol = QtWidgets.QMainWindow()
    ui = Ui_ITCcontrol()
    ui.setupUi(ITCcontrol)
    ITCcontrol.show()
    sys.exit(app.exec_())

