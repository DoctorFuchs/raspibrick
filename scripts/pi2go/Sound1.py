# Sound1.py

from raspibrick import *
robot = Robot()

for v in range(50, 110, 10):
    print v
    robot.setSoundVolume(v)
    robot.playTone(1000, 1000)
    Tools.delay(1000)

print "All done"
