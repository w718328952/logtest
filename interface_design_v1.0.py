"""
Author:Seamus
Last edit:July 2018
Function:create a interface
Vision:V1.0

"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon


class MainWindows(QWidget):
	def __init__(self):
		super().__init__()
		# 界面绘制交给initUI方法
		self.init_ui()

	def init_ui(self):

		# 设置窗口的位置和大小
		self.setGeometry(300, 200, 400, 300)
		# 设置窗口的标题
		self.setWindowTitle('AutoTest')
		# 设置窗口的图标，引用当前目录下的LOGO.png图片
		self.setWindowIcon(QIcon('LOGO.bmp'))

		self.show()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	m_windows = MainWindows()
	sys.exit(app.exec_())
