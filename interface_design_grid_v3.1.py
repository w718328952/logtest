"""
Author:Seamus
Last edit:July 2018
Function:create a interface
Vision:V3.1
New Function:This example shows a grid position.

"""

import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout,
							 QPushButton, QApplication)


class Example(QWidget):

	def __init__(self):
		super().__init__()

		self.initUI()

	# 表格布局将空间划分为行和列。我们使用QGridLayout类创建一个网格布局。
	def initUI(self):

		grid = QGridLayout()
		self.setLayout(grid)
		names = ['输入电压', '输入电流', '输出电压', '输出电流', '输入功率', '输出功率', '效率']
		positions = [(i, j) for i in range(1) for j in range(7)]
		for position, name in zip(positions, names):

			if name == '':
				continue
			button = QPushButton(name)
			button.move(300, 150)
			grid.addWidget(button, *position)

		self.setWindowTitle('Calculator')
		self.show()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())
