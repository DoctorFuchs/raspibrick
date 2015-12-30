# Ultrasonic1a.py
# Events

from raspibrick import *

def onFar(value):
    print "far event with v:", value

def onNear(value):
    print "near event with v:", value

#uss = UltrasonicSensor(far = onFar, near = onNear) # deferred registering
robot = Robot()
uss = UltrasonicSensor(far = onFar, near = onNear)
while not isEscapeHit():
    Tools.delay(100)
robot.exit()