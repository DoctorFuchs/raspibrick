# Ultrasonic1.py

from raspibrick import *

robot = Robot()
us = UltrasonicSensor()

while not isEscapeHit():
    v = us.getDistance()
    print v
    Tools.delay(1000)
robot.exit()