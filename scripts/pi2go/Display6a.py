# Display6a.py
# Ticker test, ctor parameter

from raspibrick import *
import time

robot = Robot()
dp = Display()
ip = "x192-168-1-13"
dp.showTicker(ip, count = 2, speed = 4, blocking = True)
time.sleep(3)
dp.showText("IdLE")
time.sleep(3)
robot.exit()
print "all done"
