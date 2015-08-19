# Button2.py

from raspibrick import *

robot = Robot()
Led.setColorAll(255, 255, 0)
while not robot.isEscapeHit():
    if robot.isEnterHit():
        print "enter"
    if robot.isUpHit():
        print "up"
    elif robot.isDownHit():
        print "down"
    elif robot.isLeftHit():
        print "left"
    elif robot.isRightHit():
        print "right"
robot.exit()
