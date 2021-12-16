# UFDC-1 Raspberry Pi 3 Interface
The library included in this repo allows a Raspberry Pi 3 to interface with the [UFDC-1 IC from MMS Electronics](https://www.mmselectronics.co.uk/products/sensors/frequency/ufdc-1-sensor-to-digital-transducer-serial-spi-and-i2c-interface-pdil). This IC can perform over a dozen different measurements on one or two square waves, including frequency, period, and phase shift. The UFDC-1 offers RS232, SPI, and I2C communication channels. For my purposes, connecting the chip to a Raspberry Pi via SPI made the most sense. At the very least, using this library is an easy and effective way to test out the functionality of the UFDC-1 before integrating it into another system.
### Physical Connections
The diagram shown here describes the connections required to allow the UFDC-1 to communicate with the Raspberry Pi via SPI.

![UFDC-1 Connection Diagram for Raspi 3](https://github.com/ssieglaff/UFDC1-with-Raspberry-Pi/blob/main/UFDC-1%20Raspi%203%20Connection%20Diagram.png)

There are a few things to note. If you are only measuring a single signal (for instance, a single square wave output by some sensor), there is no need to include connections for the Frequency to Measure 2 signal shown. However, as per the [datasheet](https://www.mmselectronics.co.uk/images/datasheets/sensors/UTI/UFDC_notes.pdf) each used signal must be fed into both of the respective FX and ST pins, not just one or the other.

The TXD and SDA pins must be tied to ground, or else the UFDC-1 will assume these signals are used to communicate and the SPI bus won't function properly.

The SS pin (pin 16) of the UFDC-1 can be connected to one of two pins on the Raspberry Pi 3, since it offers two seperate SPI Chip Enable pins (other Raspberry Pi models may have more or less options). When using the Python library, you will specify which CE pin you are using as either 0 (CE0, pin 24 on the Raspi) or 1 (CE1, pin 26 on the Raspi). All the other pins are locked and cannot be changed, since the Raspberry Pi 3 only has one SPI port.
### Using the Code
The Python library abstracts all the SPI communication and some of the data interperetation into a single class. Looking at the Python script "UFDC1_example.py" in this repo should give a pretty good idea of how to use the library. All of the functions in the class correspond to the commands shown in Table 5 on page 12 of the [datasheet](https://www.mmselectronics.co.uk/images/datasheets/sensors/UTI/UFDC_notes.pdf), except for the function "get_result_decimal()" which returns the measurement value from the UFDC-1 as a floating point decimal instead of a byte array. The code from "UFDC1_example.py" is shown below.
```
from UFDC1 import UFDC1

ufdc = UFDC1(0) # Use CE0 on the Raspi
ufdc.set_accuracy(7)
ufdc.set_measuring_mode(0)

print("Accuracy set to " + str(ufdc.get_accuracy()))
print("Measuring mode set to " + str(ufdc.get_measuring_mode()))

ufdc.start_measurement()

while(ufdc.is_measurement_done()):
	pass

print("Result of measurement: " + str(ufdc.get_result_decimal()) + " Hz")
```
