# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_panel_v1.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtWidgets import *

import serial
import threading
import config
import Serial_Card_Msg
import GPIO_Control
import RPi.GPIO as GPIO

#serial, sock, db 통신 연결을 위한 config 파일 load
cfg = config.Env_Config()

#pyQT5 ui 파일 로드
ui_form = uic.loadUiType("main_panel.ui")[0]
#시간 표시하기 위한 타이머
timer = QTimer()

GPIO_DO = [2,3,17,18,27,22,23,24]
GPIO_DI = [11,7,6,16,19,20,26,21]


#불필요한 WARNING 제거
GPIO.setwarnings(False)
        
#GPIO 핀의 번호모드 설정
GPIO.setmode(GPIO.BCM)
		
#GPIO_INPUT 핀 설정
for channel in GPIO_DI:
	GPIO.setup([channel], GPIO.IN)
			
#GPIO_OUTPUT 핀 설정
for channel in GPIO_DO:
	GPIO.setup([channel], GPIO.OUT, initial=GPIO.LOW)


##화면1에서 화면2 전환 방법
'''
		current_page = self.stackedWidget.currentIndex()
		self.stackedWidget.setCurrentIndex(current_page+1)
'''


class MainWindow(QMainWindow, ui_form):

	INDEX_CARD1 = 1
	card1_connect = False
	card1_id = 12345678
	card1_car_num = "서울1234"
	
	INDEX_CARD2 = 2
	card2_connect = False
	card2_id = 87654321
	card2_car_num = "서울1234"

	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.setFixedSize(800, 480)
		
		#현재 시간 디스플레이 
		self.currentDateTime = QDateTime.currentDateTime() # 시간 받아옴
		self.dateTimeEdit.setDateTime(self.currentDateTime) # 받아온 시간을 GUI 에 표시
		
		#시간 표시하기 위한 Timer
		timer.start(1000)
		timer.timeout.connect(self.cb_timeout) #1초마다 timeout 이벤트가 발생하며, timeout 함수를 호출함
		timer.timeout.connect(self.in1)
		timer.timeout.connect(self.in2)
		timer.timeout.connect(self.out1)
		timer.timeout.connect(self.out2)
		
		#종료 버튼 활성화
		self.pushButton_exit1.clicked.connect(QCoreApplication.instance().quit)
		
		#화면1 ON/OFF 버튼 활성화
		self.pushButton_silo1.clicked.connect(self.pushButton_silo1_func)
		self.pushButton_silo2.clicked.connect(self.pushButton_silo2_func)

		self.pushButton_ok1.clicked.connect(self.pushButton_ok1_func)
		self.pushButton_ok2.clicked.connect(self.pushButton_ok2_func)

		self.pushButton_silo1.setEnabled(True)
		self.pushButton_silo2.setEnabled(True)
		self.pushButton_ok1.setEnabled(False)
		self.pushButton_ok2.setEnabled(False)


		#self.gpio = GPIO_Control.GPIO_Control()
		
		#serial 통신 연결 시도
		try:
			card1_ser = serial.Serial(cfg.CARD1, 9600, timeout=0.2)
			# 시리얼 데이터 읽는 쓰레드 생성
			card1_recv = Serial_Card_Msg.CardMsgRecvThread(card1_ser, self.INDEX_CARD1)
			
			#serial 통신을 처리하는 각 쓰레들로부터 데이터를 받을 경우 처리하는 콜백함수 등록
			card1_recv.recv_cplt.connect(self.cb_serial_card_recv_cplt)
			card1_recv.start()
			
		except (OSError, serial.SerialException):
			print('CARD1 통신 포트 연결 실패!! ')
			
		try:
			card2_ser = serial.Serial(cfg.CARD2, 9600, timeout=0.2)
			# 시리얼 데이터 읽는 쓰레드 생성
			card2_recv = Serial_Card_Msg.CardMsgRecvThread(card2_ser, self.INDEX_CARD2)
			
			#serial 통신을 처리하는 각 쓰레들로부터 데이터를 받을 경우 처리하는 콜백함수 등록
			card2_recv.recv_cplt.connect(self.cb_serial_card_recv_cplt)
			card2_recv.start()
			
		except (OSError, serial.SerialException):
			print('CARD2 통신 포트 연결 실패!! ')

		
	#CARD 리더기 시리얼 통신으로 부터 데이터가 정상적으로 수신되면 호출되는 함수
	@pyqtSlot(int, str)
	def cb_serial_card_recv_cplt(self, thread_index, card_id):
		try:
			if thread_index == self.INDEX_CARD1:

				self.card1_connect = True
				self.card1_car_num = "1234"
				self.card1_id = card_id

				print('(recv data) card_id1 :', self.card1_id)
					
				#DB에 등록되어 있는 카드 데이터가 들어오면, GUI에 표시함
				if self.card1_connect == True:
					
					self.textEdit_card1.setText(self.card1_id)
					print("ok!")
					self.pushButton_ok1.setEnabled(True)
					self.pushButton_ok2.setEnabled(True)
					
			elif thread_index == self.INDEX_CARD2:

				self.card2_connect = True
				self.card2_car_num = "5678"
				self.card2_id = card_id

				print('(recv data) card_id2 :', self.card2_id)
	
				#DB에 등록되어 있는 카드 데이터가 들어오면, GUI에 표시함
				if self.card2_connect == True:
					
					self.textEdit_card2.setText(self.card2_id)
					print("ok!")
					self.pushButton_ok1.setEnabled(True)
					self.pushButton_ok2.setEnabled(True)
					
				
		except:
			pass

	def in1(self):		
		if GPIO.input(GPIO_DI[0]):
			self.input_Led1.setStyleSheet("Color:red;")
		else:
			self.input_Led1.setStyleSheet("Color:blue;")
	def in2(self):		
		if GPIO.input(GPIO_DI[1]):
			self.input_Led2.setStyleSheet("Color:red;")
		else:
			self.input_Led2.setStyleSheet("Color:blue;")
	def out1(self):	
		if GPIO.output(GPIO_DO[0]):
			self.output_Led1.setStyleSheet("Color:red;")
		else:
			self.output_Led1.setStyleSheet("Color:blue;")
	def out2(self):
		if GPIO.output(GPIO_DO[1]):
			self.output_Led2.setStyleSheet("Color:red;")
		else:
			self.output_Led2.setStyleSheet("Color:blue;")
			
	def cb_timeout(self):
		self.currentDateTime = QDateTime.currentDateTime() # 시간 받아옴
		self.dateTimeEdit.setDateTime(self.currentDateTime) # 받아온 시간을 GUI 에 표시
	
	#카드 리더기로 데이터가 읽히고, DB에 정상 조회되면 버튼이 활성화 된다.
	#여기다가 처리할 로직 넣으면 됨
	def pushButton_silo1_func(self):
		self.pushButton_silo1.setEnabled(False)
		self.pushButton_silo2.setEnabled(True)
		
	def pushButton_silo2_func(self):
		self.pushButton_silo1.setEnabled(True)
		self.pushButton_silo2.setEnabled(False)

	'''def pushButton_ok1_func(self):
			current_page = self.stackedWidget.currentIndex()
			self.stackedWidget.setCurrentIndex(current_page+1)

	def pushButton_ok2_func(self):
			current_page = self.stackedWidget.currentIndex()
			self.stackedWidget.setCurrentIndex(current_page+1)'''


if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	h_window = MainWindow()
	h_window.show()
	ret = app.exec_()
	
	#타이머 종료
	timer.stop()
	sys.exit(ret)

