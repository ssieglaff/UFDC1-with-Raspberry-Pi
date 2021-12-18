from UFDC1 import UFDC1

ufdc = UFDC1(0) # Use CE0 on the Raspi
ufdc.set_accuracy(7)
ufdc.set_measuring_mode(0)

print("Accuracy set to " + str(ufdc.get_accuracy()))
print("Measuring mode set to " + str(ufdc.get_measuring_mode()))

ufdc.start_measurement()

while(not ufdc.is_measurement_done()):
	pass

print("Result of measurement: " + str(ufdc.get_result_decimal()) + " Hz")
