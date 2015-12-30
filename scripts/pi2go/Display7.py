# Display7.py
# Blinker test, default ctor

from raspibrick import *
import time

robot = Robot()
dp = Display()
text = "boot"
dp.showBlinker(text)
while dp.isBlinkerAlive():
    continue
time.sleep(3)
dp.showText("Bye")
time.sleep(3)
robot.exit()
print "all done"
