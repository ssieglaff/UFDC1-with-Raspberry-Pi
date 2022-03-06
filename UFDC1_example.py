from UFDC1 import UFDC1

ufdc = UFDC1(0) # Use CE0 on the Raspi
ufdc.set_accuracy(7)
ufdc.set_measuring_mode(0)

print("Accuracy set to " + str(ufdc.get_accuracy()))
print("Measuring mode set to " + str(ufdc.get_measuring_mode()))


# Example of a non-delaying measurement
ufdc.start_measurement()

while not ufdc.is_measurement_done():
	# Other stuff could be done here
	pass

print("Result of the first measurement: " + str(ufdc.get_result_decimal()) + " Hz")

# Example of a delaying measurement
measurement_result = ufdc.complete_measurement()

print("Result of the second measurement: " + str(measurement_result) + " Hz")

# Call close at the end
ufdc.close()
