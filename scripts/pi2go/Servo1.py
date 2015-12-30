# Servo1.py
# Servo test

from raspibrick import *

id = 3
robot = Robot()
servo = ServoMotor(id, 350, 2)
Tools.delay(3000)

for pos in range(-50, 55, 10):
    print pos
    servo.setPos(pos)
    Tools.delay(1000)

print "all done"
robot.exit()
