# Gear1.py

from raspibrick import *

robot = Robot()
gear = Gear()
gear.forward(2000)
robot.exit()
print "All done"