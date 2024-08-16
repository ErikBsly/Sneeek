import numpy as np 
import sys
import getpass

from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtCore import QTimer, pyqtSignal, pyqtSlot, QByteArray
from PyQt5.QtNetwork import QHostAddress, QTcpServer, QTcpSocket

# keys for chaning directions
KEY_MAPPING = {
    QtCore.Qt.Key_Up: "keypress,up",
    QtCore.Qt.Key_Down: "keypress,down",
    QtCore.Qt.Key_Right: "keypress,right",
    QtCore.Qt.Key_Left: "keypress,left"
}


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("design.ui", self)
        #self.setWindowIcon(QtGui.QIcon("jo.ico"))
        # vars
        self.randomTimer = QTimer()
        self.socket = QTcpSocket()
        self.DataSocket = QTcpSocket()
        self.gridSize = None
        self.gridColors = None
        self.rawData = b''
        # connects
        self.pushButtonRequestStart.clicked.connect(self.updateGameCanvas)
        self.pushButtonConnectToHost.clicked.connect(self.connectToHost)
        self.checkBoxReady.stateChanged.connect(self.readyStateChanged)
        self.lineEditChatline.returnPressed.connect(self.sendChatMsg)
        self.pushButtonRequestStart.clicked.connect(self.startButtonPressed)
        #self.randomTimer.timeout.connect(self.updateGameCanvas)
        # setup stuff
        self.initGameCanvas()
        #self.randomTimer.start(10)
        self.lineEditName.setText(getpass.getuser())

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


    @pyqtSlot()
    def reconnectToHost(self):
        self.socket.disconnect()
        self.pushButtonConnectToHost.click()


    @pyqtSlot()
    def connectToHost(self):
        ip = self.lineEditHostIP.text().strip()
        port = 8000
        self.socket.connectToHost(ip, port)

        if not self.socket.connected:
            print("Connection failed :(")
        else:
            print("Connected to Host")
            self.socket.readyRead.connect(self.readBuffer)

            self.writeToHost("playername,{}".format(self.lineEditName.text()))
            self.readyStateChanged()


    @pyqtSlot()
    def sendChatMsg(self):
        self.writeToHost("chatmsg,"+self.lineEditChatline.text())
        self.lineEditChatline.clear()


    @pyqtSlot()
    def writeToHost(self, msg):
        if not msg: return
        if msg[-1] != "\r": msg += "\r"
        self.socket.write(msg.encode())


    @pyqtSlot()
    def readyStateChanged(self):
        msg = "ready,1" if self.checkBoxReady.isChecked() else "ready,0"
        self.writeToHost(msg)


    @pyqtSlot()
    def startButtonPressed(self):
        self.writeToHost("startgame")


    @pyqtSlot()
    def readBuffer(self):
        # append to buffer if there is some leftover from the last transmission
        self.rawData += self.socket.readAll()
        
        # every command ends with "\r"
        commands = self.rawData.split(b'\r')
        # if command transmission was not finished, so it can be completed on the next incoming transmission
        self.rawData = commands[-1]
        if commands[-1] != b'':
            del commands[-1]            

        for command in commands:
            # when image data is sent
            if command[0:6] == b'canvas': # b'...': bytes
                offset = 9 + len(str(self.gridSize[0])) + len(str(self.gridSize[1]))
                self.gridColors = np.frombuffer(command[offset:], np.uint8).reshape(*self.gridSize, 3)

                self.qimg = QImage(self.gridColors.data, self.gridColors.shape[1], self.gridColors.shape[0], self.gridColors.strides[0], QImage.Format_RGB888)
                self.updateGameCanvas()
            else:
                # print(command)
                msg = str(command, encoding="utf-8")
                
                if msg.startswith("gridsize"):
                    self.gridSize = (int(msg.split(",")[1]), int(msg.split(",")[2]))
                    self.gridColors = np.zeros((*self.gridSize, 3), dtype=np.uint8)
                    #print("Grid size: {} x {}".format(*self.gridSize))
                elif msg.startswith("gameover"):
                    print("Game over!")
                elif msg.startswith("scoreboard"):
                    self.tableWidget_Dashboard.clearContents()
                    items = msg.split(",")[1:]
                    if len(items) % 6 != 0: # 3 + 3tuple
                        print("warning: not 6 items")
                        continue # if some error occurs...
                    n = len(items) // 6
                    names, scores, isreadys, colors = [""]*n, [0]*n, [0]*n, [0]*n
                    
                    for i in range(n):
                        names[i], scores[i], isreadys[i], colors[i] = items[i*6], items[i*6+1], items[i*6+2] == "True", (int(items[i*6+3]), int(items[i*6+4]), int(items[i*6+5]))

                    # sort player stats by score
                    idx = np.flip(np.argsort(scores))
                    names, scores, isreadys, colors = [names[i] for i in idx], [scores[i] for i in idx], [isreadys[i] for i in idx], [colors[i] for i in idx]

                    for i in range(n):
                        self.tableWidget_Dashboard.setItem(i, 0, QTableWidgetItem(names[i]))
                        self.tableWidget_Dashboard.setItem(i, 1, QTableWidgetItem(str(scores[i])))
                        self.tableWidget_Dashboard.setItem(i, 2, QTableWidgetItem("ready" if isreadys[i] else ""))

                elif msg.startswith("chatmsg"):
                    self.textBrowserChat.append(msg[8:])



    @pyqtSlot()
    def keyPressEvent(self, event):
        msg = KEY_MAPPING.get(event.key(), None)

        if msg:
            self.writeToHost(msg)






# # # # # # # # # # # # # # # # # # # # #

def main():
    app = QApplication(sys.argv)
    main_window = MyApp()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()