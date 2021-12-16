import time
import spidev
#import RPi.GPIO as GPIO

spi = spidev.SpiDev()
dummy = 0xFF

class UFDC1:
	def __init__(self, ss_pin):
		self.spi = spidev.SpiDev()
		self.dummy = 0xFF
		self.spi.open(0, ss_pin)
		self.spi.max_speed_hz = 500000
		self.spi.mode = 3
	def get_accuracy(self):
		buffer = self.spi.xfer([1, self.dummy, self.dummy])
		return buffer[2]
	def set_accuracy(self, accuracy):
		self.spi.writebytes2([2, accuracy])
	def is_measurement_done(self):
		buffer = self.spi.xfer([3, self.dummy, self.dummy])
		return buffer[2] == 0
	def get_measuring_mode(self):
		buffer = self.spi.xfer([5, self.dummy, self.dummy])
		return buffer[2]
	def set_measuring_mode(self, mode):
		self.spi.writebytes2([6, mode])
	def get_result_bcd(self):
		command = [self.dummy for i in range(15)]
		command[0] = 7
		buffer = self.spi.xfer(command)
		buffer.pop(0)
		buffer.pop(0)
		return buffer
	def get_result_binary(self):
		command = [self.dummy for i in range(14)]
		command[0] = 8
		buffer = self.spi.xfer(command)
		buffer.pop(0)
		buffer.pop(0)
		return buffer
	def get_result_decimal(self):
		result = self.get_result_binary()
		i = ""
		f = ""
		for byte in result[:(len(result)//2)]:
			i = i + format(byte, "08b")
		for byte in result[(len(result)//2):]:
			f = f + format(byte, "08b")
		return int(i, 2) + int(f, 2) / 2.**len(f)
	def start_measurement(self):
		self.spi.writebytes2([9])
	def get_modulation_rotor_gradations(self):
		buffer = self.spi.xfer([11, self.dummy, self.dummy])
		return buffer[2]
	def set_modulation_rotor_gradations(self, gradations):
		self.spi.writebytes2([12, gradations])


if __name__ == "__main__":
	#GPIO.setmode(GPIO.BCM)
	ufdc = UFDC1(0)
	ufdc.set_accuracy(7)
	ufdc.set_measuring_mode(0)
	ufdc.set_modulation_rotor_gradations(69)
	print("Accuracy:         " + str(ufdc.get_accuracy()))
	print("Measuring mode:   " + str(ufdc.get_measuring_mode()))
	print("Rotor gradations: " + str(ufdc.get_modulation_rotor_gradations()))
	print("Beginning Measurement...")
	ufdc.start_measurement()
	start_time = time.time()
	while(ufdc.is_measurement_done()):
		pass
	stop_time = time.time()
	print("Measurement completed in " + str(stop_time - start_time) + " seconds.")
	print("Result of measurement: " + str(ufdc.get_result_decimal()) + " Hz")


