# LightSensor2.py

from gpanel import *
import smbus
import time

def readData(port = 0):
    if port == 0:
        adc_address = 0x48
    elif port == 1:    
        adc_address = 0x4D
    rd = bus.read_word_data(adc_address, 0)
    data = ((rd & 0xFF) << 8) | ((rd & 0xFF00) >> 8)
    data = data >> 2
    return data

makeGPanel(-10, 110, -30, 330)
drawGrid(0, 100, 0, 300)
bus = smbus.SMBus(1) 

while True:
    v = readData(1)  # adapt to your ADC (0 or 1)
    print v

