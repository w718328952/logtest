"""
Author:Seamus
Last edit:July 2018
Function:create a interface
Vision:V3.0
New Function:This example shows a label on a window using absolute positioning or relative positioning.

"""

import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QToolTip, QLabel, QPushButton,
							 QLineEdit, QTextEdit, QApplication, QMessageBox, QDesktopWidget)
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
		replay = QMessageBox.question(self, 'Message', "Are you sure to <b>Quit</b> ?",
									  QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
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

	# 创建一个网格布局(仅能单独使用，使用方法参加V3.1)
	def grid_layout(self):
		grid = QGridLayout()
		self.setLayout(grid)
		names = ['输入电压', '输入电流', '输出电压', '输出电流', '输入功率', '输出功率', '效率']
		positions = [(i, j) for i in range(1) for j in range(7)]
		for position, name in zip(positions, names):

			if name == '':
				continue
			button = QPushButton(name, self)
			button.move(300, 150)
			grid.addWidget(button, *position)

	def line_text_layout(self):

		title = QLabel('Title')
		author = QLabel('Author')
		review = QLabel('Review')

		title_edit = QLineEdit()
		author_edit = QLineEdit()
		review_edit = QTextEdit()

		grid = QGridLayout()
		grid.setSpacing(10)

		grid.addWidget(title, 1, 0)
		grid.addWidget(title_edit, 1, 1)

		grid.addWidget(author, 2, 0)
		grid.addWidget(author_edit, 2, 1)

		grid.addWidget(review, 3, 0)
		grid.addWidget(review_edit, 3, 1, 5, 1)

		self.setLayout(grid)

	# 在窗口中添加pushbutton插件的方法(绝对位置)
	def push_button(self):
		# 这种静态的方法设置一个用于显示工具提示的字体。我们使用10px滑体字体。
		QToolTip.setFont(QFont('SansSerif', 10))
		# 创建一个提示，我们称之为set tooltip()方法。我们可以使用丰富的(b粗体i斜体)文本格式
		self.setToolTip('This is a <i><b>QWidget</i></b> widget.')

		# 创建一个'开始'的PushButton并为他设置一个tooltip
		btn = QPushButton('开始', self)
		btn.setToolTip('This is a <i><b>PushButton</i></b> widget.')
		# btn.sizeHint()显示默认尺寸
		btn.resize(btn.sizeHint())
		# 移动btn在窗口中的位置
		btn.move(300, 450)

		# 创建一个'退出'的PushButton并为他设置一个tooltip
		q_btn = QPushButton('退出', self)
		q_btn.setToolTip('This is a <i><b>PushButton</i></b> widget.')
		# 为pushbutton创建一个关联程序.quit
		q_btn.clicked.connect(QCoreApplication.instance().quit)
		q_btn.resize(q_btn.sizeHint())
		q_btn.move(700, 450)

	# 使用HBoxLayout和QVBoxLayout并添加伸展因子，在窗口的右下角显示两个按钮（相对位置）
	def box_layout(self):
		# 添加两个按钮
		ok_button = QPushButton("OK")
		cancel_button = QPushButton("Cancel")
		# 创建一个水平布局和添加一个伸展因子，推动他们靠右显示
		h_box = QHBoxLayout()
		h_box.addStretch(1)
		h_box.addWidget(ok_button)
		h_box.addWidget(cancel_button)
		# 创建一个垂直布局，并添加伸展因子，让水平布局显示在窗口底部
		v_box = QVBoxLayout()
		v_box.addStretch(1)
		v_box.addLayout(h_box)
		# 设置窗口的布局界面
		self.setLayout(v_box)

	# 在窗口中添加Label插件的方法(绝对位置)
	def label(self):

		# 添加3个Label插件
		lab1 = QLabel('电压（V）：', self)
		lab1.move(15, 10)
		lab2 = QLabel('电流（A）：', self)
		lab2.move(15, 40)
		lab3 = QLabel('功率（W）：', self)
		lab3.move(15, 70)

	def init_ui(self):

		# # 设置窗口的位置和大小
		# self.setGeometry(300, 300, 250, 150)
		# 设置窗口大小
		self.resize(1000, 500)
		# 设置窗口位置
		self.window_place()
		# 设置窗口的标题
		self.setWindowTitle('AutoTest')
		# 设置窗口的图标，引用当前目录下的LOGO.png图片
		self.setWindowIcon(QIcon('LOGO.png'))

		# 1、调用添加Label的方法
		self.label()
		# 2、调用添加pushbutton的方法
		self.push_button()
		# 3、调用添加box_layout的方法
		self.box_layout()
		# # 4、调用添加line&text的方法（不可与1/2/3/5同时使用）
		# self.line_text_layout()
		# # 5、调用添加grid_layout的方法（不可与1/2/4/5同时使用）
		# self.grid_layout()

		# 创建窗口
		self.show()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	m_windows = MainWindows()
	sys.exit(app.exec_())
