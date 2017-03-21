# ADC3c.py
# Read ADC and show graphics

import smbus
import time
from gpanel import *

dt = 0.1

def readData():
    adc_address = 0x4D
    rd = bus.read_word_data(adc_address, 0)
    data = ((rd & 0xFF) << 8) | ((rd & 0xFF00) >> 8)
    data = data >> 2
    return data

def init():
    clear()
    setPenColor("gray")
    drawGrid(0, 10, 0, 1.0)
    setPenSize(2)
    setPenColor("blue")
            
bus = smbus.SMBus(1)
makeGPanel(-1, 11, -0.1, 1.1)
t = -1

while True:
    v = readData() / 1023.0 
    if t == -1 or t > 10:
        init()
        t = 0
        pos(0, v)
    else:   
        draw(t, v)
    t += dt
    time.sleep(dt)

