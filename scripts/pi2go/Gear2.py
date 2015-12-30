# Gear2.py

from raspibrick import *

robot = Robot()
gear = Gear()
gear.forward()
while not isEscapeHit():
    continue
robot.exit()
print "All done"