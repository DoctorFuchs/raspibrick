# Ultrasonic1.py

from raspibrick import *

robot = Robot()
uss = UltrasonicSensor()
n = 0
while not isEscapeHit():
    v = uss.getValue()
    print "n:  ", v
    n += 1
    Tools.delay(1000)
robot.exit()
