# Display4.py

from raspibrick import *

robot = Robot()

display = Display()
#robot.ticker("1234567890")
#Tools.delay(5000)
#robot.ticker("1234567890", 2)
#Tools.delay(15000)
display.ticker("1234567890", 2, 8)
Tools.delay(10000)
robot.exit()
print "All done"
