# UFDC-1 Raspberry Pi SPI Interface
The library included in this repo allows a Raspberry Pi to interface with the [UFDC-1 IC from MMS Electronics](https://www.mmselectronics.co.uk/products/sensors/frequency/ufdc-1-sensor-to-digital-transducer-serial-spi-and-i2c-interface-pdil). This IC can perform over a dozen different measurements on one or two square waves, including frequency, period, and phase shift. The UFDC-1 offers RS232, SPI, and I2C communication channels. For my purposes, connecting the chip to a Raspberry Pi via SPI made the most sense. At the very least, using this library is an easy and effective way to test out the functionality of the UFDC-1 before integrating it into another system.

Edit: I have also successfully used this library on a Raspberry Pi Zero W, which has a very similar pinout to the Raspberry Pi 3. I am now confident enough to say that this code *should* work with little to no modification on most Raspberry Pi models, as long as attention is payed to any differences in SPI pinout.
### Physical Connections
The diagram shown here describes the connections required to allow the UFDC-1 to communicate with the Raspberry Pi via SPI.

![UFDC-1 Connection Diagram for Raspi 3](https://github.com/ssieglaff/UFDC1-with-Raspberry-Pi/blob/main/UFDC-1%20Raspi%203%20Connection%20Diagram.png)

There are a few things to note. If you are only measuring a single signal (for instance, a single square wave output by some sensor), there is no need to include connections for the `Frequency to Measure 2` signal shown. However, as per the [datasheet](https://www.mmselectronics.co.uk/images/datasheets/sensors/UTI/UFDC_notes.pdf), each used signal must be fed into both of the respective FX and ST pins, not just one or the other.

The TXD and SDA pins must be tied to ground, or else the UFDC-1 will assume these signals are used to communicate and the SPI bus won't function properly.

The SS pin (pin 16) of the UFDC-1 can be connected to one of two pins on the Raspberry Pi 3, since it offers two seperate SPI Chip Enable pins (other Raspberry Pi models may have more or less options). When using the Python library, you will specify which CE pin you are using as either 0 (CE0, pin 24 on the Raspi) or 1 (CE1, pin 26 on the Raspi). All the other pins are locked and cannot be changed, since the Raspberry Pi 3 only has one SPI port.

An additional note is that the UFDC-1 has an automated calibration mode to help correct for inaccurate crystal oscillators. However, this mode requires the use of the RS232 interface, and since the Raspberry Pi 3 doesn't have an RS232 port I neglected to include a way to perform this calibration. In addition, the calibration mode requires the use of another accurate frequency measurment tool like an oscilloscope, which diminishes the convenience of connecting to the Raspberry Pi anyways.
### About the Code
This Python library abstracts all the SPI communication and some of the data interperetation into a single class. All that needs to be done is to get `UFDC1.py` onto a Raspberry Pi 3 and make the physical connections as specified above. All of the functions in the `UFDC1` class correspond to the commands shown in Table 5 on page 12 of the [datasheet](https://www.mmselectronics.co.uk/images/datasheets/sensors/UTI/UFDC_notes.pdf), except for the functions `get_result_decimal()`, which returns the measurement value from the UFDC-1 as a floating point decimal instead of as a byte array, `complete_measurement()`, which starts a measurement, waits until it is ready, and then returns the result as a floating point decimal, and `close()`, which closes the SPI channel and should be called at the end of the script as cleanup.
### Running the code
Looking at `UFDC1_example.py` in this repo should give a pretty good idea of how to use the library in your own python scripts.

The code from `UFDC1_example.py` can be seen here:
```
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
```

When calling `complete_measurement()`, the call will start the measurement, wait for it to complete, and then return the value. This inherantly causes a delay about equal to the time it takes for the measurement to complete (depends on the accuracy setting, see table 3 in the [datasheet](https://www.mmselectronics.co.uk/images/datasheets/sensors/UTI/UFDC_notes.pdf)). To perform other computations or actions during that time delay, you will have to do something like the non-delaying example, where you can test whether or not the measurement is done yet in a loop with other instructions.

Assuming you have made the proper electrical connections as described above and the files are situated together in the same folder like this...
```
pi@raspberrypi:~/ProjectFolder $ ls
UFDC1_example.py  UFDC1.py
```
... or `UFDC1.py` has been saved somewhere in the Python path, then running `UFDC1_example.py` should yield the following results:
```
pi@raspberrypi:~/ProjectFolder $ python UFDC1_example.py
Accuracy set to 7
Measuring mode set to 0
Result of the first measurement: 0.0 Hz
Result of the second measurement: 0.0 Hz
pi@raspberrypi:~/ProjectFolder $ 
```
The "0.0 Hz" would look different if you have a square wave signal of some kind hooked up to the first input of the chip, and should reflect a measurement in Hertz of the frequency of the signal accurate to within .005% (the accuracy of mode 7, as seen on table 3 of the [datasheet](https://www.mmselectronics.co.uk/images/datasheets/sensors/UTI/UFDC_notes.pdf)).

From this point, you should be able to modify `UFDC1_example.py` or write your own script to suit your needs.