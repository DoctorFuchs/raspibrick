# Display1a.py

from raspibrick import *

print "starting"
robot = Robot()
display = Display()
display.showText("0")
Tools.delay(3000)
display.showText("1", pos = 0, dp = [1])
Tools.delay(3000)
display.showText("11", pos = 0, dp = [1, 1])
Tools.delay(3000)
display.showText("111", pos = 0, dp = [1, 1, 1])
Tools.delay(3000)
display.showText("1111", pos = 0, dp = [1, 1, 1, 1])
Tools.delay(3000)
robot.exit()
print "All done"
