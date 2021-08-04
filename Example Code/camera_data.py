
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
 
from PyQt5.QtCore import *
import threading
import struct
import time

# serial port에 listen하고있는 thread
class Camera_Thread(threading.Thread, QObject):


	# 카드 ID을 정상적으로 읽어냈다면, GUI로 알리기 위한 기능 emit()하면 데이터를 보낼 수 있음
	recv_cplt2 = pyqtSignal(int, str)

	def __init__(self, vs, csv, found):
		threading.Thread.__init__(self)
		QObject.__init__(self)
		self.vs = vs
		self.csv = csv
		self.found = found

	def run(self):
		
		self.running = True

		while self.running:
			# grab the frame from the threaded video stream and resize it to
			# have a maximum width of 400 pixels
			frame = self.vs.read()
			frame = imutils.resize(frame, width=600)

			# find the barcodes in the frame and decode each of the barcodes
			# 프레임에서 바코드를 찾고, 각 바코드들 마다 디코드
			barcodes = pyzbar.decode(frame)


		### Let’s proceed to loop over the detected barcodes
		# loop over the detected barcodes
			for barcode in barcodes:
				# extract the bounding box location of the barcode and draw
				# the bounding box surrounding the barcode on the image
				# 이미지에서 바코드의 경계 상자부분을 그리고, 바코드의 경계 상자부분(?)을 추출한다. 
				(x, y, w, h) = barcode.rect
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

				# the barcode data is a bytes object so if we want to draw it
				# on our output image we need to convert it to a string first
				# 바코드 데이터는 바이트 객체이므로, 어떤 출력 이미지에 그리려면 가장 먼저 문자열로 변환해야 한다.
				self.barcodeData = barcode.data.decode("utf-8")
				barcodeType = barcode.type

				# draw the barcode data and barcode type on the image
				# 이미지에서 바코드 데이터와 테입(유형)을 그린다
				text = "{} ({})".format(self.barcodeData, barcodeType)
				cv2.putText(frame, text, (x, y - 10),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

				# if the barcode text is currently not in our CSV file, write
				# the timestamp + barcode to disk and update the set
				# 현재 바코드 텍스트가 CSV 파일안에 없을경우, timestamp, barcode를 작성하고 업데이트
				if self.barcodeData not in self.found:
					self.csv.write("{},{}\n".format(datetime.datetime.now(),self.barcodeData))
					self.recv_cplt2.emit(self.barcodeData)
					self.found.add(self.barcodeData)

					# show the output frame
			cv2.imshow("Barcode Scanner", frame)
			key = cv2.waitKey(1) & 0xFF

			# if the `q` key was pressed, break from the loop
			# q를 누르면 loop를 break함
			if key == ord("q"):
				break
	def Stop(self):
		self.running = False
