# ADC1.py
# Read a value from analog input 0
# in A/D in the PCF8591P @ address 0x48

from smbus import SMBus
import sys
import RPi.GPIO as GPIO
import time

i2c_address = 0x48
channel = 0

print "starting"
bus = SMBus(1)
bus.write_byte(i2c_address, channel) # set control register
t = 0
while t <= 20:
    data = bus.read_byte(i2c_address)
    print "t =", t, "s; data = ", data
    t += 0.5
    time.sleep(0.5)  # measurement period

