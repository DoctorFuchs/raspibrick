# Button2a.py

from raspibrick import *

robot = Robot()
Led.setColorAll(255, 255, 0)
while not isEscapeHit():
    if isEnterHit():
        print "enter"
    if isUpHit():
        print "up"
    elif isDownHit():
        print "down"
    elif isLeftHit():
        print "left"
    elif isRightHit():
        print "right"
robot.exit()
print "All done"