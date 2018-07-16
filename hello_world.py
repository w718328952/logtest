# -*- coding: utf-8 -*-

"""
Py40.com PyQt5 tutorial 

In this example, we create a simple
window in PyQt5.

author: Seamus
website: py40.com 
last edited: July 2018
"""

import sys

# 这里我们提供必要的引用。基本控件位于pyqt5.qtwidgets模块中。
from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == '__main__':
	# 每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数。
	app = QApplication(sys.argv)
	# QWidget部件是pyqt5所有用户界面对象的基类。他为QWidget提供默认构造函数。默认构造函数没有父类。
	w = QWidget()
	# resize()方法调整窗口的大小。这离是250px宽150px高
	w.resize(250, 150)
	# move()方法移动窗口在屏幕上的位置到x = 300，y = 300坐标。
	w.move(300, 300)
	# 设置窗口的标题
	w.setWindowTitle('Simple')
	# 显示在屏幕上
	w.show()
