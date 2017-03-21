# Temp9800.py
# Read temperature from MCP9800 IC
'''
REG_TEMP: Temparature register layout 
MSB         b7      b6      b5      b4      b3      b2      b1      b0
Weight      sign    64      32      16      8       4       2       1

LSB         b7      b6      b5      b4      b3      b2      b1      b0
Weight      1/2     1/4     1/8     1/16    0       0       0       0

Resolution in REG_CONFIG: b5, b6
b6 = 0, b5 = 0 -> b4, b5, b6 = 0; b7 valid
b6 = 0, b5 = 1 -> b4, b5 = 0; b7, b6 valid
b6 = 1, b5 = 0 -> b4 = 0; b7, b6, b5 valid
b5 = 1, b6 = 1 -> b7, b6, b5, b4 valid
'''
import smbus
import time

REG_TEMP = 0x00    # Temperature register
REG_CONFIG = 0x01    # Configuration register

bus = smbus.SMBus(1)  # RPi revision 2 (0 for revision 1)
i2c_address = 0x48

def init():
    bus.write_byte_data(i2c_address, REG_CONFIG, 0x60) # 12 bit resolution (1/16 degrees centigrade)
    
def getTemperature():
    data = bus.read_word_data(i2c_address, REG_TEMP)
    highbyte = (data >> 8) & 0xFF
    lowbyte = data & 0xFF
    (lowbyte, highbyte) = (highbyte, lowbyte) # swap (smbus uses little endian)
    sign = 1
    if highbyte & 0x80 == 0x80: # sign bit set
        sign = -1
    temp = highbyte & 0x7F # clear sign bit   
    lowbyte = lowbyte >> 4 # shift fraction bits to right
    fraction = lowbyte / 16.0
    temp = sign * (temp + fraction)
    return temp

init()
time.sleep(1)
t = 0
while True:
    temp = getTemperature()
    print "temp: %4.1f" %(temp)
    t += 1
    time.sleep(1)

