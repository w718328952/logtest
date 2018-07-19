"""
Author:Seamus
Last edit:July 2018
Function:create a interface
Vision:V2.0
New Function:Add a Push Button

"""

import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication, QMessageBox, QDesktopWidget)
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication


class MainWindows(QWidget):
	def __init__(self):
		super().__init__()
		# 界面绘制交给initUI方法
		self.init_ui()

	# 创建关闭窗口事件提示语的方法
	def closeEvent(self, event):
		# 定义消息框，默认为NO
		replay = QMessageBox.question(self, 'Message', "Are you sure to <b>Quit</b> ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if replay == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()

	# 控制窗口显示在屏幕中心的方法
	def window_place(self):
		# 获得窗口
		wp = self.frameGeometry()
		# 获得屏幕中心点
		cp = QDesktopWidget().availableGeometry().center()
		# 显示到屏幕中心
		wp.moveCenter(cp)
		self.move(wp.topLeft())

	def init_ui(self):

		# 这种静态的方法设置一个用于显示工具提示的字体。我们使用10px滑体字体。
		QToolTip.setFont(QFont('SansSerif', 10))
		# 创建一个提示，我们称之为settooltip()方法。我们可以使用丰富的(b粗体i斜体)文本格式
		self.setToolTip('This is a <i><b>QWidget</i></b> widget.')
		# 创建一个PushButton并为他设置一个tooltip
		btn = QPushButton('Button', self)
		btn.setToolTip('This is a <i><b>PushButton</i></b> widget.')
		# btn.sizeHint()显示默认尺寸
		btn.resize(btn.sizeHint())
		# 移动btn在窗口中的位置
		btn.move(50, 50)

		q_btn = QPushButton('Quit', self)
		q_btn.setToolTip('This is a <i><b>QuitButton</i></b> widget.')
		q_btn.clicked.connect(QCoreApplication.instance().quit)
		q_btn.resize(q_btn.sizeHint())
		q_btn.move(50, 150)

		# # 设置窗口的位置和大小
		# self.setGeometry(300, 200, 400, 300)
		# 设置窗口大小
		self.resize(300, 200)
		# 设置窗口位置
		self.window_place()
		# 设置窗口的标题
		self.setWindowTitle('AutoTest')
		# 设置窗口的图标，引用当前目录下的LOGO.png图片
		self.setWindowIcon(QIcon('LOGO.png'))
		# 创建窗口
		self.show()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	m_windows = MainWindows()
	sys.exit(app.exec_())
