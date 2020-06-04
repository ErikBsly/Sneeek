# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(949, 571)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(570, 10, 291, 151))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 30, 47, 13))
        self.label.setObjectName("label")
        self.lineEditHostIP = QtWidgets.QLineEdit(self.groupBox)
        self.lineEditHostIP.setGeometry(QtCore.QRect(80, 30, 113, 20))
        self.lineEditHostIP.setObjectName("lineEditHostIP")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(210, 60, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.checkBoxReady = QtWidgets.QCheckBox(self.groupBox)
        self.checkBoxReady.setGeometry(QtCore.QRect(10, 110, 70, 17))
        self.checkBoxReady.setObjectName("checkBoxReady")
        self.pushButtonRequestStart = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonRequestStart.setGeometry(QtCore.QRect(80, 110, 75, 23))
        self.pushButtonRequestStart.setObjectName("pushButtonRequestStart")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 47, 13))
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(80, 60, 113, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.tableWidget_Dashboard = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_Dashboard.setGeometry(QtCore.QRect(570, 190, 291, 71))
        self.tableWidget_Dashboard.setObjectName("tableWidget_Dashboard")
        self.tableWidget_Dashboard.setColumnCount(0)
        self.tableWidget_Dashboard.setRowCount(0)
        self.label_DisplayImage = QtWidgets.QLabel(self.centralwidget)
        self.label_DisplayImage.setGeometry(QtCore.QRect(20, 10, 512, 512))
        self.label_DisplayImage.setStyleSheet("border: 1px solid black;")
        self.label_DisplayImage.setObjectName("label_DisplayImage")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MatrixMaster"))
        self.groupBox.setTitle(_translate("MainWindow", "Network Settings"))
        self.label.setText(_translate("MainWindow", "Host IP"))
        self.lineEditHostIP.setText(_translate("MainWindow", "127.0.0.1"))
        self.pushButton.setText(_translate("MainWindow", "Connect"))
        self.checkBoxReady.setText(_translate("MainWindow", "Ready"))
        self.pushButtonRequestStart.setText(_translate("MainWindow", "Start!"))
        self.label_2.setText(_translate("MainWindow", "Name"))
        self.label_DisplayImage.setText(_translate("MainWindow", "TextLabel"))

