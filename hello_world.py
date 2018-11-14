from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import MatplotMenu #UI目录下的MatplotMenu
import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdate
import datetime,time

Ui_MainDialog = MatplotMenu.Ui_Dialog


class MatplotMenu(QDialog,Ui_MainDialog):#创建一个会话框对象
    def __init__(self):
        super(MatplotMenu,self).__init__()
        self.title = 'Matplot测试'#设置窗体title
        self.setupUi(self)
        self._createCanvas()#创建画布
        self._createLayouts()#配置组件
        self.show()#显示组件
        self._updateFigure()#更新曲线图
        self.timer = QTimer(self)#创建定时更新定时器
        self.timer.timeout.connect(self._updateFigure)#绑定更新函数        
        self.pushButton_2.clicked.connect(self._reFresh)#按钮2绑定开始更新函数

    def closeEvent(self, event):#重写会话框关闭信号产生函数
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)#产生提醒会话界面
        if reply == QMessageBox.Yes:#如果确认
            if self.timer.isActive():#定时器激活状态
                self.timer.stop()#停止定时器
                print("停止定时器")
            else:
                print("无需停止定时器")
            event.accept()#关闭事件接受
        else:
            event.ignore()#舍弃关闭事件

    def _reFresh(self):#刷新按钮绑定函数
        if self.timer.isActive() == True:#如果定时器激活状态
            self.timer.stop()#关闭定时器
            self.pushButton_2.setText("实时更新")#设置按钮字符
            print("关闭定时器......")
        else:
            self._updateFigure()#刷新界面
            self.timer.start(30000)#开启定时器
            self.pushButton_2.setText("暂停更新")#设置按钮字符
            print("打开定时器......")

    def _updateFigure(self):
        try:
            self._showLine()#显示曲线
        except Exception as e:
            print(e)

    def _showLine(self):
        self._canvas.refreshLine()

    def _errorProcess(self):
        pass

    def _createCanvas(self):
        self.setWindowTitle(self.title)#设置title
        # self.setGeometry(self.left, self.top, self.width, self.height)
        self._canvas = PlotCanvas(self, width=5, height=4)#创建matplot对象

    def _createLayouts(self):
        layout = QHBoxLayout(self.frame)#选定frame组件
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._canvas) # 添加matplot对象到QT组件内，这是最重要的一个函数，用于将matplotlib和qt绑定

class PlotCanvas(FigureCanvas):#创建一个matplot对象
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self._Font = {
            'family': 'SimHei',
            'weight': 'bold',
            'size': 15}
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,QSizePolicy.Expanding,QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self._ax = self.figure.add_subplot(111)

    def refreshLine(self):
        x = [];y = []#这里自行创建数据
        try:
            self._ax.plot(x,y, '--r*', label="Matplot Test")#绘图
            self._ax.set_title('Matplot Test', fontdict=self._Font)
            self._ax.set_xlabel("X轴", fontdict=self._Font)
            self._ax.set_ylabel("Y轴", fontdict=self._Font)
            self._ax.xaxis.grid(True, which='major')  # x坐标轴的网格使用主刻度
            self._ax.yaxis.grid(True, which="major")
            self.draw()
        except Exception as e:
            print(e)
    def plot(self):
        import datetime
        price_list = [
            {
                "PRICE" : "0.0",
                "Time" : "2018-01-22 18:56:00"},
            {
                "PRICE": "0.16461536288261414",
                "Time": "2018-01-22 20:07:18"
            },
            {
                "PRICE": "0.0",
                "Time": "2018-01-22 20:19:30"
            },
            {
                "PRICE": "0.01397849153727293",
                "Time": "2018-01-22 20:31:50"
            }
                    ]
        Font = {'family': 'SimHei',
                'weight': 'bold',
                'size': 15}
        x = []
        y = []  # 定义两个列表
        for item in price_list:  # 逐年取出单年所有信息
            y.append(float(item["PRICE"]))  # 价格数值加入y列表
            x.append(datetime.datetime.strptime(item["Time"], "%Y-%m-%d %H:%M:%S"))
            # print(type(datetime.datetime.strptime(item["Time"], "%Y-%m-%d %H:%M:%S")))

        self._ax = self.figure.add_subplot(111)
        self._ax.plot(x,y, '--r*',label = "NH3")
        self._ax.set_title('测试曲线图',fontdict = self._Font)
        self._ax.set_xlabel("时间(\"年-月-日 小时:分:秒\")",fontdict=self._Font)
        self._ax.set_ylabel("价格($)",fontdict=self._Font)
        self._ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d %H:%M:%S'))
        self._ax.xaxis.grid(True, which='major')  # x坐标轴的网格使用主刻度
        self._ax.yaxis.grid(True, which="major")
        # self._ax.xaxis.set_xticklabels(rotation=75)
        # for label in self._ax.get_xticklabels() + self._ax.get_yticklabels():
        #     label.set_fontsize(6)
            # label.set_bbox(dict(facecolor='green', edgecolor='None', alpha=0.7))

        # self._ax.xticklabels(rotation=75)
        # self.xticks(rotation=75)
        self.draw()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MatplotMenu()#创建QT对象
    window.show()#QT对象显示
    sys.exit(app.exec_())

