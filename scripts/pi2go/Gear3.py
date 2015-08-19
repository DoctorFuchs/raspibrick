# Gear3.py

from raspibrick import *

robot = Robot()
gear = Gear()

while not isEscapeHit():
    if isUpHit():
        gear.forward()
    elif isDownHit():
        gear.stop()
    elif isLeftHit():
        gear.left()
    elif isRightHit():
        gear.right()
robot.exit()
