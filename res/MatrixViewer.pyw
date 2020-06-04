import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.figure import Figure
from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
import os, sys
import imageio

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QMessageBox
from PyQt5.QtCore import QTimer, pyqtSignal, pyqtSlot

from design import Ui_MainWindow



class MyApp(QMainWindow, Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

		self.M = [] # main img
		self.x, self.y1, self.y2 = [], [], [] # x,y for data plotting

		self.initPlots()

		# signals / slots
		self.textBrowser.fileDropped.connect(self.setNewFileName)
		self.lineEdit_xLabel.editingFinished.connect(self.pushButton_replot.click)
		self.lineEdit_yLabel.editingFinished.connect(self.pushButton_replot.click)
		self.lineEdit_plotTitle.editingFinished.connect(self.pushButton_replot.click)
		self.lineEdit_xLim.editingFinished.connect(self.pushButton_replot.click)
		self.lineEdit_yLim.editingFinished.connect(self.pushButton_replot.click)
		self.pushButton_replot.clicked.connect(self.plotMatrix)
		self.lineEditFilename.editingFinished.connect(lambda: self.setNewFileName(self.lineEditFilename.text()))


	def processFile(self):
		url = self.lineEditFilename.text()
		if url == "": return
		fname, ext = os.path.splitext(url)
		ext = ext.lower()
		
		if ext in [".png", ".jpg", ".jpeg", ".bmp"]:
			self.M = imageio.imread(url, as_gray=True)
		elif ext in [".tif", ".tiff"]:
			self.M = imageio.imread(url)
		elif ext == ".bin":
			self.M = np.fromfile(url, np.int32)
			self.M = self.M.reshape(int(np.sqrt(self.M.size)), int(np.sqrt(self.M.size))) # assume square image
		elif ext == ".npy":
			self.M = np.load(url)
		elif ext in [".dat", ".txt", ".csv"]:
			try: self.x, self.y1, self.y2 = np.genfromtxt(url, unpack=True, usecols=(0, 1, 2), filling_values=0)
			except:
				try:
					self.x, self.y1 = np.genfromtxt(url, unpack=True, usecols=(0, 1), filling_values=0);
					self.y2 = []
				except: pass

			self.M = []


	def plotMatrix(self):
		plotted = False
		# first check if data is set
		if np.any(self.M):
			self.mainFig.clf()
			self.ax_main = self.mainFig.add_subplot()
			self.mainFig.colorbar(self.ax_main.matshow(self.M))
			plotted = True
			
		elif np.any(self.x) and np.any(self.y1):
			self.mainFig.clf()
			self.ax_main = self.mainFig.add_subplot()
			if np.any(self.y2):
				self.ax_main.plot(self.x, self.y1, "darkgoldenrod", lw=1)
				self.ax_main.plot(self.x, self.y2, "mediumslateblue", lw=1)
			else:
				self.ax_main.plot(self.x, self.y1, "darkgoldenrod", lw=1)
			plotted = True

		if plotted:
			title = self.lineEdit_plotTitle.text()
			xlabel = self.lineEdit_xLabel.text()
			ylabel = self.lineEdit_yLabel.text()
			xlim_str = self.lineEdit_xLim.text()
			ylim_str = self.lineEdit_yLim.text()

			if title != "": self.ax_main.set_title(title)
			if xlabel != "": self.ax_main.set_xlabel(xlabel)
			if ylabel != "": self.ax_main.set_ylabel(ylabel)

			if xlim_str != "":
				if xlim_str.find(",") == -1:
					try: self.ax_main.set_xlim(float(xlim_str))
					except: pass
				else:
					try: self.ax_main.set_xlim(*[float(s.strip()) for s in xlim_str.split(",")])
					except: pass

			if ylim_str != "":
				if ylim_str.find(",") == -1:
					try: self.ax_main.set_ylim(float(ylim_str))
					except: pass
				else:
					try: self.ax_main.set_ylim(*[float(s.strip()) for s in ylim_str.split(",")])
					except: pass

			self.mainFig.tight_layout()
			self.img_canvas.draw()

	def initPlots(self):
		self.mainFig = plt.figure(figsize=(self.widgetMainPlot.width()/100, self.widgetMainPlot.height()/100)) 
		self.img_canvas = FigureCanvas(self.mainFig)
		#self.img_canvas.setParent(self.widgetMainPlot)
		
		self.toolbar = NavigationToolbar(self.img_canvas, self.widgetMainPlot)
		self.widgetMainPlot.setLayout(QtWidgets.QVBoxLayout(self.widgetMainPlot))
		self.widgetMainPlot.layout().addWidget(self.img_canvas)
		self.widgetMainPlot.layout().addWidget(self.toolbar)
		#layout.addWidget(self.img_canvas)
		#self.widgetMainPlot.addToolBar(QtCore.Qt.BottomToolBarArea, NavigationToolbar(self.img_canvas, self))

		self.ax_main = self.mainFig.add_subplot()
		self.x = np.linspace(-3, 3, 1000)
		self.y1 = np.cos(50*self.x)*np.exp(-self.x**2)
		self.plotMatrix()


	@pyqtSlot(str)
	def setNewFileName(self, f=""):
		# print("Slot called")
		if not f: return
		if not os.path.exists(f): return
		self.lineEditFilename.setText(f)
		self.processFile()
		self.plotMatrix()





# # # # # # # # # # # # # # # # # # # # #

def main():
	app = QApplication(sys.argv)
	main_window = MyApp()
	main_window.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()