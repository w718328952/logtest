import sys
import numpy
import random
import serial
import time
from PyQt5 import QtWidgets
from matplotlib.ticker import  MultipleLocator
import threading
import matplotlib.ticker as ticker
from datetime import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import numpy as np
from matplotlib.figure import Figure
from PyQt5 import QtGui

ser = serial.Serial()
ser.baudrate = 115200
ser.port = 'COM5'
print(ser)
ser.open()
print(ser.is_open)

class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        # FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.curveObj = None # draw object

    def plot(self, datax, datay):
        if self.curveObj is None:
            #create draw object once
            self.curveObj, = self.ax.plot_date(np.array(datax), np.array(datay),'bo-')
        else:
            #update data of draw object
            self.curveObj.set_data(np.array(datax), np.array(datay))
            #update limit of X axis,to make sure it can move

            self.ax.set_xlim(datax[0], datax[-1])
            self.ax.set_ylim(111.0, 111.4)
            self.ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.6f'))
            # ymajorLocator = MultipleLocator(1.0)
            # self.ax.yaxis.set_major_locator(ymajorLocator)

        xticklabels = self.ax.xaxis.get_ticklabels()
        for xtick in xticklabels:
            xtick.set_rotation(25)

        yticklabels = self.ax.yaxis.get_ticklabels()
        for ytick in yticklabels:
            ytick.set_rotation(1.0)

        self.draw()

class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.figure = plt.figure()
        # self.axes = self.figure.add_subplot(111)Figure' is not defined
        # We want the axes cleared every time plot() is called
        self.canvas = MplCanvas()

        self.toolbar = NavigationToolbar(self.canvas, self)
        # self.toolbar.hide()

        # Just some button
        self.button1 = QtWidgets.QPushButton('StartPlot')
        self.button1.clicked.connect(self.startplot)

        self.button2 = QtWidgets.QPushButton('Zoom')
        self.button2.clicked.connect(self.zoom)

        self.button3 = QtWidgets.QPushButton('Pan')
        self.button3.clicked.connect(self.pan)

        self.button4 = QtWidgets.QPushButton('Home')
        self.button4.clicked.connect(self.home)

        self.button5 = QtWidgets.QPushButton('Save')
        self.button5.clicked.connect(self.save)

        self.button6 = QtWidgets.QPushButton('Clear')
        self.button6.clicked.connect(self.clear)


        # set the layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        btnlayout = QtWidgets.QHBoxLayout()
        btnlayout.addWidget(self.button1)
        btnlayout.addWidget(self.button2)
        btnlayout.addWidget(self.button3)
        btnlayout.addWidget(self.button4)
        btnlayout.addWidget(self.button5)
        btnlayout.addWidget(self.button6)

        self.dataX = []
        self.dataY = []

        qw = QtWidgets.QWidget(self)
        qw.setLayout(btnlayout)
        layout.addWidget(qw)
        self.setLayout(layout)



    def getdata(self):
        return numpy.array([i for i in range (100)])

    def home(self):
        self.toolbar.home()
    def zoom(self):
        self.toolbar.zoom()
    def pan(self):
        self.toolbar.pan()
    def save(self):
        self.toolbar.save_figure()

    def startplot(self):
        ''' plot some random stuff '''
        # data = self.getdata()
        self.tData = threading.Thread(name = "dataGenerator",target=self.generateData)
        self.tData.start()

    def generateData(self):
        while 1:
              s = ser.read(10)
              print(s)
              # print(float(s))
              newTime = date2num(datetime.now())
              self.dataX.append(newTime)
              self.dataY.append(float(s))
              self.canvas.plot(self.dataX, self.dataY)
              # time.sleep(1)


    def clear(self):
        self.axes.cla()
        self.axes.set_xlabel('Frequency')
        self.axes.set_ylabel('Amplification')
        self.axes.set_title('test')
        self.tData.join()
        self.canvas.draw()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main = Window()
    main.setWindowTitle('Simple QTpy and MatplotLib example with Zoom/Pan')
    main.show()

    sys.exit(app.exec_())
