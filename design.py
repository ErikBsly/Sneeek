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
        MainWindow.setFocusPolicy(QtCore.Qt.StrongFocus)
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
        self.pushButtonConnectToHost = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonConnectToHost.setGeometry(QtCore.QRect(210, 60, 75, 23))
        self.pushButtonConnectToHost.setObjectName("pushButtonConnectToHost")
        self.checkBoxReady = QtWidgets.QCheckBox(self.groupBox)
        self.checkBoxReady.setGeometry(QtCore.QRect(10, 110, 70, 17))
        self.checkBoxReady.setObjectName("checkBoxReady")
        self.pushButtonRequestStart = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonRequestStart.setGeometry(QtCore.QRect(80, 110, 75, 23))
        self.pushButtonRequestStart.setObjectName("pushButtonRequestStart")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 47, 13))
        self.label_2.setObjectName("label_2")
        self.lineEditName = QtWidgets.QLineEdit(self.groupBox)
        self.lineEditName.setGeometry(QtCore.QRect(80, 60, 113, 20))
        self.lineEditName.setObjectName("lineEditName")
        self.tableWidget_Dashboard = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_Dashboard.setEnabled(True)
        self.tableWidget_Dashboard.setGeometry(QtCore.QRect(570, 180, 321, 131))
        self.tableWidget_Dashboard.setShowGrid(False)
        self.tableWidget_Dashboard.setRowCount(6)
        self.tableWidget_Dashboard.setColumnCount(3)
        self.tableWidget_Dashboard.setObjectName("tableWidget_Dashboard")
        self.tableWidget_Dashboard.horizontalHeader().setVisible(False)
        self.tableWidget_Dashboard.verticalHeader().setDefaultSectionSize(23)
        self.label_DisplayImage = QtWidgets.QLabel(self.centralwidget)
        self.label_DisplayImage.setGeometry(QtCore.QRect(20, 10, 514, 514))
        self.label_DisplayImage.setStyleSheet("border: 1px solid #444;")
        self.label_DisplayImage.setObjectName("label_DisplayImage")
        self.textBrowserChat = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowserChat.setGeometry(QtCore.QRect(570, 330, 321, 161))
        self.textBrowserChat.setObjectName("textBrowserChat")
        self.lineEditChatline = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditChatline.setGeometry(QtCore.QRect(570, 500, 321, 20))
        self.lineEditChatline.setObjectName("lineEditChatline")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Leets Plee Sneeek"))
        self.groupBox.setTitle(_translate("MainWindow", "Network Settings"))
        self.label.setText(_translate("MainWindow", "Host IP"))
        self.lineEditHostIP.setText(_translate("MainWindow", "127.0.0.1"))
        self.pushButtonConnectToHost.setText(_translate("MainWindow", "Connect"))
        self.checkBoxReady.setText(_translate("MainWindow", "Ready"))
        self.pushButtonRequestStart.setText(_translate("MainWindow", "Start!"))
        self.label_2.setText(_translate("MainWindow", "Name"))
        self.lineEditName.setText(_translate("MainWindow", "Dummie"))
        self.label_DisplayImage.setText(_translate("MainWindow", "Snake Canvas!"))
        self.textBrowserChat.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Chat with us! &lt;3</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))

