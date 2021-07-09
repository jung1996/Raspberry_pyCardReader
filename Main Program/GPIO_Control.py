import RPi.GPIO as GPIO #GPIO 라이브러리 불러오기

class GPIO_Control():

	def __init__(self):
		
		self.GPIO_DO = [2,3,17,18,27,22,23,24]
		self.GPIO_DI = [11,7,6,16,19,20,26,21]
		#불필요한 WARNING 제거
		GPIO.setwarnings(False)
        
		#GPIO 핀의 번호모드 설정
		GPIO.setmode(GPIO.BCM)
		
		#GPIO_INPUT 핀 설정
		for channel in self.GPIO_DI:
			GPIO.setup([channel], GPIO.IN)
			
		#GPIO_OUTPUT 핀 설정
		for channel in self.GPIO_DO:
			GPIO.setup([channel], GPIO.OUT, initial=GPIO.LOW)

	'''def gpio_write_pin(channel, pin_state):
		GPIO.output(self.GPIOIO_DO[channel], pin_state)
		
	def gpio_read_pin(channel, pin_state):
		if GPIO.input(self.GPIOIO_DI[channel]) == GPIO.LOW:
			return 0
		else:
			return 1'''
			
	'''def gpio_toggle_pin(channel):
		# STM32 에서는 OUTPUT 핀도 읽을 수 있는데, 되는지 확인 필요
		if GPIO.input(self.GPIOIO_DO[channel]) == GPIO.LOW:
			GPIO.output(self.GPIOIO_DO[channel], GPIO.HIGH)
		else:
			GPIO.output(self.GPIOIO_DO[channel], GPIO.LOW)'''
