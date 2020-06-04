import numpy as np 
import os, sys

from PyQt5 import QtWidgets, QtNetwork
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, pyqtSignal, pyqtSlot

from design import Ui_MainWindow



class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        print("jo")

        self.pushButtonRequestStart.clicked.connect(self.displayTestImage)

        self.displayTestImage()

    @pyqtSlot()
    def displayTestImage(self):
        img = np.random.randint(256, size=(256, 256, 3), dtype=np.uint8)

        self.qimg = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888)
        self.label_DisplayImage.setPixmap(QPixmap.fromImage(self.qimg))


        # img = np.random.randint(256, size=(256, 256, 3), dtype=np.uint8)
        # self.qimg_c = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format_Indexed8)
        # self.graphicsView.






















# # # # # # # # # # # # # # # # # # # # #

def main():
    app = QApplication(sys.argv)
    main_window = MyApp()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()