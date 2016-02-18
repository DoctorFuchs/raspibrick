# DidelDemo.py

import RPi.GPIO as GPIO
import smbus
import sys

from DgTell import DgTell
from DgTell1 import DgTell1
import time


try:
    if GPIO.RPI_REVISION > 1:
        bus = smbus.SMBus(1) # For revision 2 Raspberry Pi
        print "Found SMBus for revision 2"
    else:
        bus = smbus.SMBus(0) # For revision 1 Raspberry Pi
        print "Found SMBus for revision 1"
except:
   print "No SMBus found on this robot device."
   sys.exit()

displayType = ""
try:
    addr = 0x20
    rc = bus.read_byte_data(addr, 0)
    if rc != 0xA0:   # 0xA0 for didel display
        raise Exception()
    displayType = "didel1"
    print "Found display DGTell1"
except:
     print "'didel1' display not found"

if displayType == "":
    try:
        addr = 0x24
        data = [0] * 4
        bus.write_i2c_block_data(addr, data[0], data[1:])  # trying to clear display
        displayType = "didel"
        print "Found display DGTell"
    except:
        print "'didel' display not found"

if displayType == "didel":
    dp = DgTell()
elif displayType == "didel1":
    dp = DgTell1()
else:
    print "no display"
    sys.exit()

while (True):
    text = "HELO"
    dp.showBlinker(text, dp = [0, 0, 0, 0], count = 4, speed = 2, blocking = True)
    text = "dIdEL bY J-d. nicoud"
    dp.showTicker(text, count = 1, speed = 1, blocking = True)
    time.sleep(2)
    for i in range(1001):
        dp.showText("%4d" % (i))
        time.sleep(0.01)
    time.sleep(3)
    for x in range(9000, 10000):
        dp.showText("%4d" % (x), dp = [0, 1, 0, 0])
        time.sleep(0.01)
    time.sleep(3)
    dp.showText("donE")
    time.sleep(6)
