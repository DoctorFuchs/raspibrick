# Display3.py
# Scroll text to left

from raspibrick import *
import time

robot = Robot()
dp = Display()
text = "0123456789"
print "show text with", text
#rc = dT.showText(text)
#rc = dT.showText(text, 2)
rc = dp.showText(text, pos = -2)
time.sleep(3)
for i in range(10):
    nb = dp.scrollToLeft()
    print "remaining:", nb
    time.sleep(2)
robot.exit()
print "done"

