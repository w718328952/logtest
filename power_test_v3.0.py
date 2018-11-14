"""
Author:Seamus
Last edit:July 2018
Function:plot a picture
Vision:V3.0
New function:serial+ plot 2 picture

"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
from mainwindow import Ui_MainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.dates import date2num, MinuteLocator, SecondLocator, DateFormatter
import sys
import serial
import serial.tools.list_ports
from pyico import *
import time
from array import array
import random
import threading
from datetime import datetime
import re
import numpy as np

global vpa_list, ipa_list
vpa_list = []
ipa_list = []

class MainWindow(QtWidgets. QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self._createCanvas()  # 创建画布
        self._createLayouts()  # 配置组件
        self.show()  # 显示组件

        # 设置应用程序的窗口图标
        self.setWindowIcon(QIcon("LOGO.png"))

        # 串口无效
        self.ser = None
        self.send_num = 0
        self.receive_num = 0
        # 记录最后发送的回车字符的变量
        self.rcv_enter = ''

        # 显示发送与接收的字符数量
        dis = '发送：' + '{:d}'.format(self.send_num) + '  接收:' + '{:d}'.format(self.receive_num)
        self.statusBar.showMessage(dis)

        # 刷新一下串口的列表
        self.refresh()

        # 波特率
        # self.comboBox_2.addItem('256000')
        self.comboBox_2.addItem('256000')
        self.comboBox_2.addItem('115200')
        self.comboBox_2.addItem('57600')
        self.comboBox_2.addItem('56000')
        self.comboBox_2.addItem('38400')
        self.comboBox_2.addItem('19200')
        self.comboBox_2.addItem('14400')
        self.comboBox_2.addItem('9600')
        self.comboBox_2.addItem('4800')
        self.comboBox_2.addItem('2400')
        # self.comboBox_2.addItem('1200')

        # 数据位
        self.comboBox_3.addItem('8')
        self.comboBox_3.addItem('7')
        self.comboBox_3.addItem('6')
        self.comboBox_3.addItem('5')

        # 停止位
        self.comboBox_4.addItem('1')
        self.comboBox_4.addItem('1.5')
        self.comboBox_4.addItem('2')

        # 校验位
        self.comboBox_5.addItem('NONE')
        self.comboBox_5.addItem('ODD')
        self.comboBox_5.addItem('EVEN')

        # 对testEdit进行事件过滤
        self.textEdit.installEventFilter(self)

        # 实例化一个定时器
        self.timer = QTimer(self)

        self.timer_send = QTimer(self)

        self.timer_plot = QTimer(self)

        # 定时器调用读取串口接收数据
        self.timer.timeout.connect(self.recv)

        # 定时发送
        self.timer_send.timeout.connect(self.send)

        # 定时处理value数据
        # self.timer_plot.timeout.connect(self.vpa_value_processing)
        self.timer_plot.timeout.connect(self.ipa_value_processing)

        # 发送数据按钮
        self.pushButton.clicked.connect(self.send)
        # 打开关闭串口按钮
        self.pushButton_2.clicked.connect(self.open_close)

        # 刷新串口外设按钮
        self.pushButton_4.clicked.connect(self.refresh)

        # 开启绘图按钮
        self.pushButton_5.clicked.connect(self.startPlot)

        # 暂停绘图按钮
        self.pushButton_6.clicked.connect(self.pausePlot)

        # 清除窗口
        self.pushButton_3.clicked.connect(self.clear)

        # 定时发送
        self.checkBox_4.clicked.connect(self.send_timer_box)

        # 波特率修改
        self.comboBox_2.activated.connect(self.baud_modify)

        # 串口号修改
        self.comboBox.activated.connect(self.com_modify)

        # 执行一下打开串口
        self.open_close(True)
        self.pushButton_2.setChecked(True)

    # 刷新一下串口
    def refresh(self):
        # 查询可用的串口
        plist = list(serial.tools.list_ports.comports())

        if len(plist) <= 0:
            print("No used com!");
            self.statusBar.showMessage('没有可用的串口')


        else:
            # 把所有的可用的串口输出到comboBox中去
            self.comboBox.clear()

            for i in range(0, len(plist)):
                plist_0 = list(plist[i])
                self.comboBox.addItem(str(plist_0[0]))

    # 事件过滤
    def eventFilter(self, obj, event):
        # 处理textEdit的键盘按下事件
        if event.type() == event.KeyPress:

            if self.ser != None:
                if event.key() == QtCore.Qt.Key_Up:

                    # up 0x1b5b41 向上箭头
                    send_list = []
                    send_list.append(0x1b)
                    send_list.append(0x5b)
                    send_list.append(0x41)
                    input_s = bytes(send_list)

                    num = self.ser.write(input_s)
                elif event.key() == QtCore.Qt.Key_Down:
                    # down 0x1b5b42 向下箭头
                    send_list = []
                    send_list.append(0x1b)
                    send_list.append(0x5b)
                    send_list.append(0x42)
                    input_s = bytes(send_list)

                    num = self.ser.write(input_s)
                else:
                    # 获取按键对应的字符
                    char = event.text()
                    num = self.ser.write(char.encode('utf-8'))
                self.send_num = self.send_num + num
                dis = '发送：' + '{:d}'.format(self.send_num) + '  接收:' + '{:d}'.format(self.receive_num)
                self.statusBar.showMessage(dis)
            else:
                pass
            return True
        else:

            return False

    # 重载窗口关闭事件
    def closeEvent(self, e):

        # 关闭定时器，停止读取接收数据
        self.timer_send.stop()
        self.timer_plot.stop()
        self.timer.stop()

        # 关闭串口
        if self.ser != None:
            self.ser.close()

    # 定时发送数据
    def send_timer_box(self):
        if self.checkBox_4.checkState():
            time = self.lineEdit_2.text()

            try:
                time_val = int(time, 10)
            except ValueError:
                QMessageBox.critical(self, 'pycom', '请输入有效的定时时间!')
                return None

            if time_val == 0:
                QMessageBox.critical(self, 'pycom', '定时时间必须大于零!')
                return None
            # 定时间隔发送
            self.timer_send.start(time_val)

        else:
            self.timer_send.stop()

    # 清除窗口操作
    def clear(self):
        self.textEdit.clear()
        self.send_num = 0
        self.receive_num = 0
        dis = '发送：' + '{:d}'.format(self.send_num) + '  接收:' + '{:d}'.format(self.receive_num)
        self.statusBar.showMessage(dis)

    # 串口接收数据处理
    def recv(self):
        global ipa_cont, vpa_cont
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        # print(now)
        try:
            time.sleep(0.1)
            num = self.ser.inWaiting()
            # n = self.ser.readline(50)
            # print(n)
        except:

            self.timer_send.stop()
            self.timer.stop()
            self.timer_plot.stop()
            # 串口拔出错误，关闭定时器
            self.ser.close()
            self.ser = None

            # 设置为打开按钮状态
            self.pushButton_2.setChecked(False)
            self.pushButton_2.setText("打开串口")
            self.pushButton_5.setChecked(False)
            self.pushButton_5.setText("开始")
            print('serial error!')
            return None
        if (num > 0):
            # 有时间会出现少读到一个字符的情况，还得进行读取第二次，所以多读一个
            data = self.ser.read(num)

            # 调试打印输出数据
            # print(data)
            num = len(data)
            # 十六进制显示
            if self.checkBox_3.checkState():
                out_s = ''
                for i in range(0, len(data)):
                    out_s = out_s + '{:02X}'.format(data[i]) + ' '

            else:
                # 串口接收到的字符串为b'123',要转化成unicode字符串才能输出到窗口中去
                out_s = data.decode('iso-8859-1')

                if self.rcv_enter == '\r':
                    # 上次有回车未显示，与本次一起显示
                    out_s = '\r' + out_s
                    self.rcv_enter = ''

                if out_s[-1] == '\r':
                    # 如果末尾有回车，留下与下次可能出现的换行一起显示，解决textEdit控件分开2次输入回车与换行出现2次换行的问题
                    out_s = out_s[0:-1]
                    self.rcv_enter = '\r'

            # 先把光标移到到最后
            cursor = self.textEdit.textCursor()
            if (cursor != cursor.End):
                cursor.movePosition(cursor.End)
                self.textEdit.setTextCursor(cursor)

            # 把字符串显示到窗口中去
            self.textEdit.insertPlainText(now + '\n' + out_s)

            # 提取VPA和IPA值
            matchObj1 = re.compile(r'((vpa=)+(\d+)+)', re.I | re.S)
            matchObj2 = re.compile(r'((ipa=)+(\d+)+)', re.I | re.S)

            # 将VPA和IPA值存入列表中
            vpa_cont = matchObj1.findall(out_s)
            ipa_cont = matchObj2.findall(out_s)

            # 统计接收字符的数量
            self.receive_num = self.receive_num + num
            dis = '发送：' + '{:d}'.format(self.send_num) + '  接收:' + '{:d}'.format(self.receive_num)
            self.statusBar.showMessage(dis)

            # 获取到text光标
            textCursor = self.textEdit.textCursor()
            # 滚动到底部
            textCursor.movePosition(textCursor.End)
            # 设置光标到text中去
            self.textEdit.setTextCursor(textCursor)
        else:
            # 此时回车后面没有收到换行，就把回车发出去
            if self.rcv_enter == '\r':
                # 先把光标移到到最后
                cursor = self.textEdit.textCursor()
                if (cursor != cursor.End):
                    cursor.movePosition(cursor.End)
                    self.textEdit.setTextCursor(cursor)
                self.textEdit.insertPlainText('\r')
                self.rcv_enter = ''

    # 串口发送数据处理
    def send(self):
        if self.ser != None:
            input_s = self.lineEdit.text()
            if input_s != "":

                # 发送字符
                if (self.checkBox.checkState() == False):
                    if self.checkBox_2.checkState():
                        # 发送新行
                        input_s = input_s + '\r\n'
                    input_s = input_s.encode('utf-8')

                else:
                    # 发送十六进制数据
                    input_s = input_s.strip()  # 删除前后的空格
                    send_list = []
                    while input_s != '':
                        try:
                            num = int(input_s[0:2], 16)

                        except ValueError:
                            print('input hex data!')
                            QMessageBox.critical(self, 'pycom', '请输入十六进制数据，以空格分开!')
                            return None

                        input_s = input_s[2:]
                        input_s = input_s.strip()

                        # 添加到发送列表中
                        send_list.append(num)
                    input_s = bytes(send_list)
                print(input_s)
                # 发送数据
                try:
                    num = self.ser.write(input_s)
                except:

                    self.timer_send.stop()
                    self.timer.stop()
                    # 串口拔出错误，关闭定时器
                    self.ser.close()
                    self.ser = None

                    # 设置为打开按钮状态
                    self.pushButton_2.setChecked(False)
                    self.pushButton_2.setText("打开串口")
                    print('serial error send!')
                    return None

                self.send_num = self.send_num + num
                dis = '发送：' + '{:d}'.format(self.send_num) + '  接收:' + '{:d}'.format(self.receive_num)
                self.statusBar.showMessage(dis)
                # print('send!')
            else:
                print('none data input!')

        else:
            # 停止发送定时器
            self.timer_send.stop()
            QMessageBox.critical(self, 'pycom', '请打开串口')

    # 波特率修改
    def baud_modify(self):
        if self.ser != None:
            self.ser.baudrate = int(self.comboBox_2.currentText())

    # 串口号修改
    def com_modify(self):
        if self.ser != None:
            self.ser.port = self.comboBox.currentText()


    # 开启PLOT功能
    def start_plot(self, btn_sta):

        if btn_sta == True:
            time = self.lineEdit_3.text()

            try:
                time_val = int(time, 10)
            except ValueError:
                QMessageBox.critical(self, 'pycom', '请输入有效的定时时间!')
                return None

            if time_val == 0:
                QMessageBox.critical(self, 'pycom', '定时时间必须大于零!')
                return None
            # 定时间隔发送
            self.timer_plot.start(time_val)
            self.pushButton_5.setText("停止")
            print('开始测试')
            self._canvas.plot()

        else:
            self.timer_plot.stop()
            self.pushButton_5.setText("开始")
            print('结束测试')

    # 打开关闭串口
    def open_close(self, btn_sta):
        if btn_sta == True:
            try:
                # 输入time_plot参数

                self.ser = serial.Serial(self.comboBox.currentText(), int(self.comboBox_2.currentText()), timeout=0.2)
            except:
                QMessageBox.critical(self, 'pycom', '没有可用的串口或当前串口被占用')
                return None
            # 字符间隔超时时间设置
            self.ser.interCharTimeout = 0.001
            # 1ms的测试周期
            self.timer.start(2)
            self.pushButton_2.setText("关闭串口")
            print('open')
        else:
            # 关闭定时器，停止读取接收数据
            self.timer_send.stop()
            # self.timer_plot.stop()
            self.timer.stop()

            try:
                # 关闭串口
                self.ser.close()
            except:
                QMessageBox.critical(self, 'pycom', '关闭串口失败')
                return None

            self.ser = None

            self.pushButton_2.setText("打开串口")
            # self.pushButton_5.setText("停止")
            # print('停止测试')
            print('close!')


    # 返回VPA列表
    def vpa_value_processing(self):

            vpa_len = len(vpa_cont)
            if vpa_len > 0:
                for i in range(vpa_len):
                    vpa_tuple = vpa_cont[i]
                    vpa_value = vpa_tuple[2]
                    vpa_list.append(vpa_value)
            else:
                print('未采到电压值！请检查TX和RX是否PING通。')
            print(vpa_list)
            return vpa_list

    # 返回IPA列表
    def ipa_value_processing(self):

            ipa_len = len(ipa_cont)
            if ipa_len > 0:
                for i in range(ipa_len):
                    ipa_tuple = ipa_cont[i]
                    ipa_value = ipa_tuple[2]
                    ipa_list.append(ipa_value)
            else:
                print('未采到电流值！请检查串口设置是否正确。')
            print(ipa_list)
            # return ipa_list
            # self.plot_dynamic_wave()

    # 定义star/pause按钮定义
    def startPlot(self):
        ''' begin to plot'''

        self.MplCanvasWrapper.startPlot()

        pass

    def pausePlot(self):
        ''' pause plot '''

        self.MplCanvasWrapper.pausePlot()

        pass

    def releasePlot(self):
        ''' stop and release thread'''

        self.MplCanvasWrapper.releasePlot()

    # 创建plot Canvas界面
    def _createCanvas(self):
        # self.setGeometry(self.left, self.top, self.width, self.height)
        self._canvas = MplCanvas(self, width=10, height=8)#创建matplot对象

    # 创建plot layout界面
    def _createLayouts(self):
        layout = QtWidgets.QHBoxLayout(self.frame)  #选定frame组件
        layout.setContentsMargins(0, 1, 1, 1)
        layout.addWidget(self._canvas)  # 添加matplot对象到QT组件内，这是最重要的一个函数，用于将matplotlib和qt绑定

	# # 更新figure参数
    # def _updateFigure(self):
    #     try:
    #         self._showLine()#显示曲线
    #     except Exception as e:
    #         print(e)
	#
	# # 显示行代码（调用refrechline函数）
    # def _showLine(self):
    #     self._canvas.refreshLine()
	#
	# #
    # def _errorProcess(self):
    #     pass

#创建一个matplot对象
X_MINUTES = 1

Y_MAX = 100

Y_MIN = 1

INTERVAL = 1

MAXCOUNTER = int(X_MINUTES * 60 / INTERVAL)

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=10, height=8, dpi=100):
        self._Font = {
            'family': 'SimHei',
            'weight': 'bold',
            'size': 15}
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.ax = self.figure.add_subplot(111)

        self.ax.set_xlabel("time of data generator")

        self.ax.set_ylabel('random data value')

        self.ax.legend()

        self.ax.set_ylim(Y_MIN, Y_MAX)

        self.ax.xaxis.grid(True, which='major')  # x坐标轴的网格使用主刻度

        self.ax.yaxis.grid(True, which="major")

        self.ax.xaxis.set_major_locator(MinuteLocator())  # every minute is a major locator

        self.ax.xaxis.set_minor_locator(SecondLocator([10, 20, 30, 40, 50]))  # every 10 second is a minor locator

        self.ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))  # tick label formatter

        self.curveObj = None
    # draw object
    def plot(self, datax, datay):

        if self.curveObj is None:

            # create draw object once

            self.curveObj, = self.ax.plot_date(np.array(datax), np.array(datay), 'bo-')

        else:

            # update data of draw object

            self.curveObj.set_data(np.array(datax), np.array(datay))

            # update limit of X axis,to make sure it can move

            self.ax.set_xlim(datax[0], datax[-1])

        ticklabels = self.ax.xaxis.get_ticklabels()

        for tick in ticklabels:
            tick.set_rotation(25)

        self.draw()

class MplCanvasWrapper(QtWidgets.QWidget):

	def __init__(self, parent=None):

		QtWidgets.QWidget.__init__(self, parent)

		self.canvas = MplCanvas()

		self.vbl = QtWidgets.QVBoxLayout()

		self.ntb = NavigationToolbar(self.canvas, parent)

		self.vbl.addWidget(self.ntb)

		self.vbl.addWidget(self.canvas)

		self.setLayout(self.vbl)

		self.dataX = []

		self.dataY = []

		self.initDataGenerator()

	def startPlot(self):

		self.__generating = True

	def pausePlot(self):

		self.__generating = False

		pass

	def initDataGenerator(self):

		self.__generating = False

		self.__exit = False

		self.tData = threading.Thread(name="dataGenerator", target=self.generateData)

		self.tData.start()

	def releasePlot(self):

		self.__exit = True

		self.tData.join()

	def generateData(self):

		counter = 0

		while (True):

			if self.__exit:
				break

			if self.__generating:

				newData = random.randint(Y_MIN, Y_MAX)

				newTime = date2num(datetime.now())

				self.dataX.append(newTime)

				self.dataY.append(newData)

				self.canvas.plot(self.dataX, self.dataY)

				# if counter >= MAXCOUNTER:
				#
				# 	self.dataX.pop(0)
				#
				# 	self.dataY.pop(0)
				#
				# else:
				#
				# 	counter += 1

			time.sleep(INTERVAL)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
