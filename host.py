#%%
import numpy as np
import sys, os

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtCore import QTimer, pyqtSignal, pyqtSlot, QByteArray, QDataStream, QIODevice
from PyQt5.QtNetwork import QHostAddress, QTcpServer, QTcpSocket

from design_host import Ui_MainWindow

class SneeekPlayer():
    def __init__(self):
        self.ip = None
        self.color = None
        self.direction = None

    def changeDirection(self, direction):
        self.direction = direction


class SneeekGrid():
    def __init__(self, gridSize):
        self.gridSize = gridSize
        self.grid = np.zeros((*self.gridSize, 2), dtype=np.int) # 2 to assign a tuple (player, lifetime) to every grid site

    def clearGrid(self):
        self.grid.fill(0)




# https://stackoverflow.com/questions/48499713/server-client-connection-in-pyqt
# https://stackoverflow.com/questions/41167409/pyqt5-sending-and-receiving-messages-between-client-and-server
class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # vars
        self.gameTimer = QTimer()
        self.tcpServer = None

        self.gridSize = (64, 64)
        self.gameGrid = SneeekGrid(self.gridSize)

        # connect

        # init
        self.initServer()

    def initServer(self):
        self.tcpServer = QTcpServer(self)
        port = 8000
        address = QHostAddress('127.0.0.1')
        if not self.tcpServer.listen(address, port):
            print("Cant listen on port {}".format(port))
            self.close()
        else:
            print("Creating server...")
            self.tcpServer.newConnection.connect(self.dealCommunication)

    def dealCommunication(self):
        print("Dealing with new communication")
        # Get a QTcpSocket from the QTcpServer
        clientConnection = self.tcpServer.nextPendingConnection()
        # instantiate a QByteArray
        block = QByteArray()
        # QDataStream class provides serialization of binary data to a QIODevice
        out = QDataStream(block, QIODevice.ReadWrite)
        # We are using PyQt5 so set the QDataStream version accordingly.
        out.setVersion(QDataStream.Qt_5_0)
        out.writeUInt16(0)
        # this is the message we will send it could come from a widget.
        message = "Goodbye!"
        # get a byte array of the message encoded appropriately.
        message = bytes(message, encoding='ascii')
        # now use the QDataStream and write the byte array to it.
        out.writeString(message)
        out.device().seek(0)
        out.writeUInt16(block.size() - 2)
        # wait until the connection is ready to read
        clientConnection.waitForReadyRead()
        # read incomming data
        instr = clientConnection.readAll()
        # in this case we print to the terminal could update text of a widget if we wanted.
        print(str(instr, encoding='ascii'))
        # get the connection ready for clean up
        clientConnection.disconnected.connect(clientConnection.deleteLater)
        # now send the QByteArray.
        clientConnection.write(block)
        # now disconnect connection.
        clientConnection.disconnectFromHost()


# # # # # # # # # # # # # # # # # # # # #

def main():
    app = QApplication(sys.argv)
    main_window = MyApp()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()