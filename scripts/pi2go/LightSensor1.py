# LightSensor1.py

from raspibrick import *

robot = Robot()
ls = LightSensor(LS_FRONT_LEFT)
while not robot.isButtonHit():
    v = ls.getValue()
    print "v:", v
    Tools.delay(100)
robot.exit()
print "All done"