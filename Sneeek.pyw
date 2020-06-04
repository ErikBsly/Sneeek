import numpy as np 
import os, sys

from PyQt5 import QtWidgets, QtNetwork, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtCore import QTimer, pyqtSignal, pyqtSlot

from design import Ui_MainWindow



class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #self.setWindowIcon(QtGui.QIcon("jo.ico"))
        # vars
        self.randomTimer = QTimer()
        
        # connects
        self.pushButtonRequestStart.clicked.connect(self.updateGameCanvas)
        self.randomTimer.timeout.connect(self.updateGameCanvas)
        # setup stuff
        self.initGameCanvas()
        self.fillTable()
        #self.randomTimer.start(10)

    def initGameCanvas(self):
        #img = np.random.randint(256, size=(64, 64, 3), dtype=np.uint8)
        img = 255*np.ones((64, 64, 3), dtype=np.uint8)

        self.qimg = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888)
        self.label_DisplayImage.setPixmap(QPixmap.fromImage(self.qimg).scaled(512, 512))


        # img = np.random.randint(256, size=(256, 256, 3), dtype=np.uint8)
        # self.qimg_c = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format_Indexed8)
        # self.graphicsView.

    @pyqtSlot()
    def updateGameCanvas(self):
        c1 = QColor(255, 0, 0) # red
        c2 = QColor(0, 128, 0) # red

        rows = np.random.randint(64, size=15)
        cols = np.random.randint(64, size=15)
        for r, c in zip(rows, cols):
            self.qimg.setPixelColor(r, c, c1)

        rows = np.random.randint(64, size=15)
        cols = np.random.randint(64, size=15)
        for r, c in zip(rows, cols):
            self.qimg.setPixelColor(r, c, c2)

        self.label_DisplayImage.setPixmap(QPixmap.fromImage(self.qimg).scaled(512, 512))

    def fillTable(self):
        self.tableWidget_Dashboard.setItem(0, 0, QTableWidgetItem("Navajo"))
        self.tableWidget_Dashboard.setItem(0, 1, QTableWidgetItem("120"))
        self.tableWidget_Dashboard.setItem(1, 0, QTableWidgetItem("Buslow"))
        self.tableWidget_Dashboard.setItem(1, 1, QTableWidgetItem("99"))




















# # # # # # # # # # # # # # # # # # # # #

def main():
    app = QApplication(sys.argv)
    main_window = MyApp()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()