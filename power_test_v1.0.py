#!/usr/bin/python
# -*- coding: <encoding name> -*-
#coding=utf8

import serial
import time
import csv
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import string


def plot_picture(dir_value):

	x = np.arange(0.0, 10, 0.1)

	plt.plot(x, [y == dir_value for y in x], label='power', linewidth=4, color='black')
	plt.axis([0, 15, -1, 50])
	plt.xlabel("time/min", fontsize=20)
	plt.ylabel('power/w')
	plt.title('TX power')
	plt.legend(loc='upper left')
	plt.grid(True)
	plt.savefig('TX power.pdf', dpi=200)

	print(mpl.rcParams['savefig.dpi'])  # default to 100              the size of the pic will be 800*600

	# print mpl.rcParams['interactive']




def receive_dispose(rx_str):

	rx_list = []
	# print(rx_str)
	rx_name = rx_str.split('=')[0]
	# print(str(rx_name))

	if rx_name == 'V1 ':
		rx_value = rx_str.split('=')[-1].split(' ')[1]
		rx_list.append((rx_name, rx_value))
	elif rx_name == 'I1 ':
		rx_value = rx_str.split('=')[-1].split(' ')[1]
		rx_list.append((rx_name, rx_value))
	elif rx_name == 'V2 ':
		rx_value = rx_str.split('=')[-1].split(' ')[1]
		rx_list.append((rx_name, rx_value))
	elif rx_name == 'I2 ':
		rx_value = rx_str.split('=')[-1].split(' ')[1]
		rx_list.append((rx_name, rx_value))
	elif rx_name == 'V3 ':
		rx_value = rx_str.split('=')[-1].split(' ')[1]
		rx_list.append((rx_name, rx_value))
	elif rx_name == 'V4 ':
		rx_value = rx_str.split('=')[-1].split(' ')[1]
		rx_list.append((rx_name, rx_value))
	else:
		rx_list = []

	return rx_list



def save_file():

	with open("./test_data.csv", 'a', newline='') as wf:
		writer = csv.writer(wf)
		for row in range(1):
			writer.writerow(file_data_tuple)

	wf.close()


class MSerialPort:

	def __init__(self, port, baud):
		self.port = serial.Serial(port, baud, timeout=0.5)
		if not self.port.isOpen():
			self.port.open()

	def port_open(self):
		if not self.port.isOpen():
			self.port.open()

	def port_close(self):
		self.port.close()

	def send_data(self, data):
		number = self.port.write(data)
		return number

	def read_data(self, bit):
		while True:
			data = self.port.readline(bit)
			return data


if __name__ == '__main__':

	header = ['Ipa', 'Vtemp', 'CH1_I', 'CH2_VIN', 'CH2_VOUT', 'CH2_I']
	with open('test_data.csv', 'w', encoding='utf-8', newline='') as f:
		f_csv = csv.DictWriter(f, header)
		f_csv.writeheader()
		# f_csv.writerows()
	f.close()

	mSerial = MSerialPort('COM6', 9600)

	while True:
		time.sleep(1)
		rx = mSerial.read_data(50)
		rx_str = rx.decode('utf-8')
		file_data = receive_dispose(rx_str)

		# print(dir_name)
		if file_data != []:
			file_data_tuple = file_data[0]
			dir_name = file_data_tuple[0]
			dir_value = file_data_tuple[1]
			print(dir_value)
			plot_picture(dir_value)

		# print(file_data)

