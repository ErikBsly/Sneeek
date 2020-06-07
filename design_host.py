# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design_host.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(945, 548)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_DisplayImage = QtWidgets.QLabel(self.centralwidget)
        self.label_DisplayImage.setGeometry(QtCore.QRect(20, 10, 514, 514))
        self.label_DisplayImage.setStyleSheet("border: 1px solid #444;")
        self.label_DisplayImage.setObjectName("label_DisplayImage")
        self.pushButtonRestart = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonRestart.setGeometry(QtCore.QRect(550, 10, 191, 71))
        self.pushButtonRestart.setStyleSheet("font-size: 24pt;")
        self.pushButtonRestart.setObjectName("pushButtonRestart")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Host Sneeek"))
        self.label_DisplayImage.setText(_translate("MainWindow", "Snake Canvas!"))
        self.pushButtonRestart.setText(_translate("MainWindow", "Restart"))

