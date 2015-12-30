# LightSensor1a.py
# Event

from raspibrick import *


def onDark(id, value):
    print "dark event at", id, "with v:", value

def onBright(id, value):
    print "bright event", id, "with v:", value

#ls = LightSensor(LS_FRONT_LEFT, bright = onBright, dark = onDark) # deferred register
robot = Robot()
ls = LightSensor(LS_FRONT_LEFT, bright = onBright, dark = onDark)
while not robot.isEscapeHit():
    Tools.delay(100)
robot.exit()
print "All done"