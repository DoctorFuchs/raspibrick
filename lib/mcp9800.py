# mcp9800.py
# Read temperature from MCP9800 IC
'''
REG_TEMP: Temperature register layout 
MSB         b7      b6      b5      b4      b3      b2      b1      b0
Weight      sign    64      32      16      8       4       2       1

LSB         b7      b6      b5      b4      b3      b2      b1      b0
Weight      1/2     1/4     1/8     1/16    0       0       0       0

Resolution in REG_CONFIG: b5, b6
b6 = 0, b5 = 0 -> REG_TEMP: b4 = b5 = b6 = 0; b7 valid (1/2 degrees resolution)
b6 = 0, b5 = 1 -> REG_TEMP: b4 = b5 = 0; b7, b6 valid (1/4 degrees resolution)
b6 = 1, b5 = 0 -> REG_TEMP: b4 = 0; b7, b6, b5 valid (1/8 degrees resolution)
b5 = 1, b6 = 1 -> REG_TEMP: b7, b6, b5, b4 valid (1/16 degrees resolution)
'''
import smbus

REG_TEMP = 0x00    # Temperature register
REG_CONFIG = 0x01  # Configuration register
_bus = smbus.SMBus(1)  # RPi revision 2 (0 for revision 1)

def init(i2c_address = 0x48,  resolution = 3):
    global _i2c_address
    _i2c_address = i2c_address
    if resolution == 0: # 1/2 degress
        config = 0x00
    elif resolution == 1: # 1/4 degrees
        config = 0x20
    elif resolution == 2: # 1/8 degrees
        config = 0x40        
    elif resolution == 3: # 1/16 degrees
        config = 0x60        
    _bus.write_byte_data(i2c_address, REG_CONFIG, config)
    
def getTemperature():
    data = _bus.read_word_data(_i2c_address, REG_TEMP)
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
    return int((temp * 10)) / 10  # rounded to 1 decimal

