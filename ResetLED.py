# ResetLED.py

from raspibrick import *

print "ResetLED starting...",
robot = Robot()
Led.clearAll()
robot.exit()
print "Done"

