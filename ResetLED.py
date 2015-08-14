# ResetLED.py

from raspibrick import *

print "ResetLED starting...",
robot = Robot()
display = Display()
display.clear()
Led.clearAll()
robot.exit()
print "Done"

