# ADC2.py
# Read a value from analog channel 0
# in A/D in the PCF8591P @ address 0x48
# Data shown at 7-segment display
# Button to terminate

from smbus import SMBus
import sys
import time
from Disp4tronix import Disp4tronix
from ButtonLib import *

def myButtonListener(event):
    global isRunning
    isRunning = False

i2c_address = 0x48
dp = Disp4tronix()

print "starting"
channel = 0
bus = SMBus(1) # For revision 2 Raspberry Pi
bus.write_byte(i2c_address, channel) # set control register
setButtonPin(12)
addButtonListener(myButtonListener)
data_old = -1
isRunning = True
while isRunning:
    data = bus.read_byte(i2c_address)
    if data != data_old:
         dp.showText("%4d" %data) # right adjusted
         data_old = data
    time.sleep(0.1)  # needed because multiplexed display uses processing power!!
dp.showText("donE")
time.sleep(3)
dp.clear()  # needed to stop the display thread