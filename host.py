#%%
import numpy as np
import sys, os

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtCore import QTimer, pyqtSignal, pyqtSlot, QByteArray, QDataStream, QIODevice
from PyQt5.QtNetwork import QHostAddress, QTcpServer, QTcpSocket

from design_host import Ui_MainWindow

class SneeekPlayer:
    def __init__(self):
        self.id = None
        self.name = None
        self.color = QColor(0, 0, 255)
        self.v = "up"
        self.socket = None
        self.isReady = False
        self.length = 1
        self.pos = None
        self.alive = True
        # self.vstr = {
        #     "up": np.array([-1, 0]),
        #     "down": np.array([1, 0]),
        #     "left": np.array([0, -1]),
        #     "right": np.array([0, 1])
        # }

    def write(self, msg):
        if not self.socket.connected: return
        self.socket.write(msg)






class SneeekGrid:
    def __init__(self, gridSize):
        self._gridSize = gridSize
        # self.grid = np.zeros((*self._gridSize, 2), dtype=np.int) # 2 to assign a tuple (player, lifetime) to every grid site
        self.grid = np.zeros(self._gridSize, dtype=np.int)
        self.owner = -1 * np.ones(self._gridSize, dtype=np.int)

    def clearGrid(self):
        self.grid.fill(0)

    def setRandom(self):
        self.grid = np.random.default_rng().integers(256, size=self._gridSize, dtype=np.uint8)

    def randomEmptyField(self):
        pos = np.random.default_rng().integers(self._gridSize[1]), np.random.default_rng().integers(self._gridSize[0])
        # print(pos, " ", self.grid.shape, " ", self.grid[pos])
        while self.grid[pos] != 0:
            pos = np.random.default_rng().integers(self._gridSize[1]), np.random.default_rng().integers(self._gridSize[0])
        return pos

    def placeTarget(self):
        self.grid[self.randomEmptyField()] = -1

    def reduceLifeTimeByOne(self):
        self.grid[self.grid > 0] -= 1
        # remove ownership of expired sites
        self.owner[self.grid == 0] = -1






class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # vars
        self.gameTimer = QTimer()
        self.gameTimer.start(50)
        self.Server = None
        self.player = []

        self.gridSize = (64, 64)
        self.gameGrid = SneeekGrid(self.gridSize)
        self.gridColors = np.zeros((*self.gridSize, 3), dtype=np.uint8)
        self.gameHasStarted = True
        self.lengthGainPerEat = 3

        # connect
        self.gameTimer.timeout.connect(self.processGameStep)

        # init
        self.initGame()
        self.initServer()

        #self.gameTimer.start(200)

    def initServer(self):
        self.Server = QTcpServer(self)
        address = QHostAddress('127.0.0.1')
        port = 8000
        if self.Server.listen(address, port):
            print("Creating server...")
            self.Server.newConnection.connect(self.handleNewConnection)
        else:
            print("Can't listen on port {}".format(port))
            self.close()

    def initGame(self):
        self.gameGrid.clearGrid()
        self.gameGrid.placeTarget()

    @pyqtSlot()
    def handleNewConnection(self):
        print("New incoming connection")        
        # find first unused id
        new_id, ids = len(self.player), [self.player[i].id for i in range(len(self.player))]
        for i in range(len(self.player)):
            if i not in ids:
                new_id = i
                break
        # new index of player array: id != idx 
        idx = len(self.player)
        self.player.append(SneeekPlayer())
        # Get a QTcpSocket from the QTcpServer
        self.player[idx].socket = self.Server.nextPendingConnection()
        if self.player[idx].socket.connected:
            print("from {}".format(self.player[idx].socket.peerAddress().toString()))
            self.player[idx].socket.readyRead.connect(self.readBuffer)
            self.player[idx].socket.disconnected.connect(self.handleDisconnection)

            self.player[idx].id = new_id
            self.player[idx].name = "abc"
            self.player[idx].color = np.random.default_rng().integers(128, 255, size=3)
            self.player[idx].pos = self.gameGrid.randomEmptyField()

            self.gameGrid.grid[self.player[idx].pos] = 1
            self.gameGrid.owner[self.player[idx].pos] = self.player[idx].id
           
            self.writeToClients("gridsize,{},{}".format(*self.gameGrid._gridSize))

    @pyqtSlot()
    def handleDisconnection(self):
        sender = self.sender()

        for i in range(len(self.player)):
            if self.player[i].socket == sender:
                print("Disconnection of player {} with ip {}".format(self.player[i].id, self.player[i].socket.peerAddress().toString()))
                del self.player[i]

    @pyqtSlot()
    def readBuffer(self):
        sender = self.sender()
        # find which palyer has sent the signal. Then convert one-element list to scalar
        idx = [i for i,p in enumerate(self.player) if p.socket == sender][0]


        rawData = self.player[idx].socket.readAll()
        if rawData.isEmpty(): return
        msg = str(rawData, encoding="utf-8")
        # print(msg)

        if msg.startswith("keypress"):
            self.player[idx].v = msg.split(",")[1]

        if msg.startswith("playername"):
            self.player[idx].name = msg.split(",")[1]

        if msg.startswith("ready"):
            self.player[idx].isReady = True if msg.split(",")[1]=="1" else False # ready,1 or ready,0

    @pyqtSlot()
    def writeToClients(self, msg, encode=True):
        if encode: msg = msg.encode()
        for i in range(len(self.player)):
            self.player[i].socket.write(msg)
       

    def sendImageToClients(self):
        prefix = "canvas,{},{},".format(*self.gameGrid._gridSize).encode()
        content = self.gridColors.tobytes()
        self.writeToClients(prefix+content, encode=False)

    def sendScoreBoardToClients(self):
        msg = "scoreboard"
        for i in range(len(self.player)):
            msg += ",{},{},{},{}".format(self.player[i].name, self.player[i].score, self.player[i].isReady, self.player[i].color)

        self.writeToClients(msg)


    def processGameStep(self):

        if self.gameHasStarted:
            self.gameGrid.reduceLifeTimeByOne()

            for i in range(len(self.player)):
                if self.player[i].alive:
                    v, pos, newpos = self.player[i].v, self.player[i].pos, None
                    #-------- shorten that stuff into one if statement!
                    if v in ["up", "down"]:
                        newy = pos[0]+1 if v == "down" else pos[0]-1
                        newpos = newy, self.player[i].pos[1]
                        if not 0 <= newy < self.gridSize[0]:
                            self.player[i].alive = False
                            print("Player {} game over".format(self.player[i].id))
                            continue
                        elif self.gameGrid.grid[newpos] > 0:
                            self.player[i].alive = False
                            print("Player {} game over".format(self.player[i].id))
                            continue
                    #--------------------------------------
                    if v in ["left", "right"]:
                        newx = pos[1]+1 if v == "right" else pos[1]-1
                        newpos = self.player[i].pos[0], newx
                        if not 0 <= newx < self.gridSize[1]: 
                            self.player[i].alive = False
                            print("Player {} game over".format(self.player[i].id))
                            continue
                        elif self.gameGrid.grid[newpos] > 0:
                            self.player[i].alive = False
                            print("Player {} game over".format(self.player[i].id))
                            continue
                    #--------------------------------------
                    # eat!
                    if self.gameGrid.grid[newpos] == -1:
                        self.player[i].length += self.lengthGainPerEat
                        self.gameGrid.grid[self.gameGrid.owner == self.player[i].id] += self.lengthGainPerEat
                        self.gameGrid.placeTarget()

                    self.player[i].pos = newpos

                    self.gameGrid.grid[self.player[i].pos] = self.player[i].length
                    self.gameGrid.owner[self.player[i].pos] = self.player[i].id


        color_food = (0, 0, 0) # black
        blue = (0, 0, 255)

        self.gridColors.fill(255) # all white

        self.gridColors[self.gameGrid.grid == -1] = color_food
        self.gridColors[self.gameGrid.owner == 0] = blue



        self.sendImageToClients()

# # # # # # # # # # # # # # # # # # # # #

def main():
    app = QApplication(sys.argv)
    main_window = MyApp()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
