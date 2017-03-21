# Infrared3.py

import smbus
import time
from py7seg import Py7Seg
from Beeper import Beeper

# u = mx + b, x = 1/d
m = 19.8
b = 0.228
P_BEEPER = 22

def readData():
    adc_address = 0x4D
    rd = bus.read_word_data(adc_address, 0)
    data = ((rd & 0xFF) << 8) | ((rd & 0xFF00) >> 8)
    data = data >> 2
    return data
                    
bus = smbus.SMBus(1)
ps = Py7Seg()
beeper = Beeper(P_BEEPER)
beeper.start(0.05, 0.2, 3, True) # to say we are ready
beeper.start(0, 0)
while True:
    v = readData()
    u = v / 1023.0 * 5
    print u
    d = int(m / (u - b))
    print "d =" ,d, "cm"
    if d > 0 and d < 50:
        ps.showText("%4d" %d)
        beeper.setOnOffTime(0.05, 0.01 * d)
    else:
        ps.showText("----")
        beeper.setOnTime(0)
    time.sleep(0.1)    

