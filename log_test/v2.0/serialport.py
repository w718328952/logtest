
import time
import re




# class SerialPort_Ctrol(object):
#
#     def __init__(self):
#         global vpa_list, ipa_list
#         self.ser = None
#         # self.vpa_cont = None
#         # self.ipa_cont = None
#         self.ipa_list = []
#         self.vpa_list = []
#
#     def recv(self):
#         global ipa_cont, vpa_cont
#
#         try:
#             time.sleep(0.1)
#             num = self.ser.inWaiting()
#             # n = self.ser.readline(50)
#             # print(n)
#         except:
#
#             return None
#
#         if (num > 0):
#             # 有时间会出现少读到一个字符的情况，还得进行读取第二次，所以多读一个
#             data = self.ser.read(num)
#
#             # 调试打印输出数据
#             # print(data)
#             num = len(data)
#             out_s = data.decode('iso-8859-1')
#             if self.rcv_enter == '\r':
#                 # 上次有回车未显示，与本次一起显示
#                 out_s = '\r' + out_s
#                 self.rcv_enter = ''
#
#             if out_s[-1] == '\r':
#                 # 如果末尾有回车，留下与下次可能出现的换行一起显示，解决textEdit控件分开2次输入回车与换行出现2次换行的问题
#                 out_s = out_s[0:-1]
#                 self.rcv_enter = '\r'
#
#
#             # 提取VPA和IPA值
#             matchObj1 = re.compile(r'((vpa=)+(\d+)+)', re.I | re.S)
#             matchObj2 = re.compile(r'((ipa=)+(\d+)+)', re.I | re.S)
#
#             # 将VPA和IPA值存入列表中
#             vpa_cont = matchObj1.findall(out_s)
#             ipa_cont = matchObj2.findall(out_s)
#
#     # 返回VPA列表
#     vpa_list = []
#     def vpa_value_processing(self):
# 			#
#             # vpa_len = len(vpa_cont)
#             # if vpa_len > 0:
#             #     for i in range(vpa_len):
#             #         vpa_tuple = vpa_cont[i]
#             #         vpa_value = vpa_tuple[2]
#             #         vpa_list.append(vpa_value)
#             # else:
#             #     print('未采到电压值！请检查TX和RX是否PING通。')
#             vpa_list = ['22', '33']
#             print(vpa_list)
#             return sum(vpa_list) / len(vpa_list)
#
#     # 返回IPA列表
#     def ipa_value_processing(self):
#
#             ipa_len = len(ipa_cont)
#             if ipa_len > 0:
#                 for i in range(ipa_len):
#                     ipa_tuple = ipa_cont[i]
#                     ipa_value = ipa_tuple[2]
#                     ipa_list.append(ipa_value)
#             else:
#                 print('未采到电流值！请检查串口设置是否正确。')
#             print(ipa_list)
#             return sum(ipa_list) / len(ipa_list)

