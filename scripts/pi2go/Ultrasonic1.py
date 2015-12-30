# Ultrasonic1.py

from raspibrick import *

robot = Robot()
uss = UltrasonicSensor()
n = 0
while not isEscapeHit():
    v = uss.getValue()
    print "n:  ", v
    n += 1
robot.exit()
print "All done"
