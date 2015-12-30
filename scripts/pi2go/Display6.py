# Display6.py
# Ticker test, default ctor

from raspibrick import *
import time

robot = Robot()
dp = Display()
ip = "x192-168-1-13"
dp.showTicker(ip)
while dp.isTickerAlive():
    continue
dp.showText("IdLE")
time.sleep(3)
robot.exit()
print "all done"
