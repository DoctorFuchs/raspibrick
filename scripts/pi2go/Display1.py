# Display1.py

from raspibrick import *

robot = Robot()
display = Display()
display.showText("1234")
Tools.delay(3000)
display.showText("1234567890")
Tools.delay(3000)
display.showText("1234567890", pos = 2)
Tools.delay(3000)
display.showText("1234567890", pos = -2)
Tools.delay(3000)
display.showText("1234567890", pos = 1, dp = [1, 1, 0, 0])
Tools.delay(3000)
display.showText("1234567890", pos = 1, dp = [0, 1])
Tools.delay(3000)
robot.exit()
print "All done"
