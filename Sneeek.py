import numpy as np 
import os, sys

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtCore import QTimer, pyqtSignal, pyqtSlot, QByteArray
from PyQt5.QtNetwork import QHostAddress, QTcpServer, QTcpSocket

from design import Ui_MainWindow



class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #self.setWindowIcon(QtGui.QIcon("jo.ico"))
        # vars
        self.randomTimer = QTimer()
        self.socket = QTcpSocket()
        self.DataSocket = QTcpSocket()
        self.gridSize = None
        self.gridColors = None
        # connects
        self.pushButtonRequestStart.clicked.connect(self.updateGameCanvas)
        self.pushButtonConnectToHost.clicked.connect(self.connectToHost)
        self.checkBoxReady.stateChanged.connect(self.readyStateChanged)
        #self.randomTimer.timeout.connect(self.updateGameCanvas)
        # setup stuff
        self.initGameCanvas()
        self.fillTable()
        #self.randomTimer.start(10)

    def initGameCanvas(self):
        #img = np.random.randint(256, size=(64, 64, 3), dtype=np.uint8)
        img = 255*np.ones((64, 64, 3), dtype=np.uint8) # white!

        self.qimg = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888)
        self.label_DisplayImage.setPixmap(QPixmap.fromImage(self.qimg).scaled(512, 512))


    @pyqtSlot()
    def updateGameCanvas(self):
        # c = QColor(0, 128, 0) # darkgreen
        # for r, c in np.random.randint(64, size=(15,2)): self.qimg.setPixelColor(r, c, 2)
        self.label_DisplayImage.setPixmap(QPixmap.fromImage(self.qimg).scaled(self.label_DisplayImage.size()))

    def fillTable(self):
        self.tableWidget_Dashboard.setItem(0, 0, QTableWidgetItem("Navajo"))
        self.tableWidget_Dashboard.setItem(0, 1, QTableWidgetItem("120"))
        self.tableWidget_Dashboard.setItem(1, 0, QTableWidgetItem("Buslow"))
        self.tableWidget_Dashboard.setItem(1, 1, QTableWidgetItem("99"))

    @pyqtSlot()
    def connectToHost(self):
        ip = self.lineEditHostIP.text()
        port = 8000
        self.socket.connectToHost(ip, port)

        if not self.socket.connected:
            print("Connection failed :(")
            return
        else:
            print("Connected to Host")
            self.socket.readyRead.connect(self.readBuffer)

            playerName = self.lineEditName.text()
            self.writeToHost("playername,{}".format(playerName))

    @pyqtSlot()
    def writeToHost(self, msg):
        if not msg: return
        self.socket.write(msg.encode())

    @pyqtSlot()
    def readyStateChanged(self, state):
        msg = "ready,1" if state else "ready,0"
        self.writeToHost(msg)

    @pyqtSlot()
    def readBuffer(self):
        rawData = self.socket.readAll()
        if rawData.isEmpty(): return

        # when image data is sent
        if rawData[0:6] == b'canvas': # b'...': bytes
            # start after 3rd comma!!!
            self.gridColors = np.frombuffer(rawData[13:], np.uint8).reshape((*self.gridSize), 3)

            #a, b = np.random.randint(64, size=2)
            # print(self.gridColors[a,b])
            #self.gridColors[a, b] = [255, 255, 255]

            self.qimg = QImage(self.gridColors.data, self.gridColors.shape[1], self.gridColors.shape[0], self.gridColors.strides[0], QImage.Format_RGB888)
            self.updateGameCanvas()
            return
        
        msg = str(rawData, encoding="utf-8")
        

        if msg.startswith("gridsize"):
            self.gridSize = (int(msg.split(",")[1]), int(msg.split(",")[2]))
            self.gridColors = np.zeros((*self.gridSize, 3), dtype=np.uint8)
            print("Grid size: {} x {}".format(*self.gridSize))



    @pyqtSlot()
    def keyPressEvent(self, event):
        key = event.key()
        msg = ""
        if key == QtCore.Qt.Key_Up:    msg = "keypress,up"
        if key == QtCore.Qt.Key_Down:  msg = "keypress,down"
        if key == QtCore.Qt.Key_Right: msg = "keypress,right"
        if key == QtCore.Qt.Key_Left:  msg = "keypress,left"

        if msg: self.writeToHost(msg)













# # # # # # # # # # # # # # # # # # # # #

def main():
    app = QApplication(sys.argv)
    main_window = MyApp()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()