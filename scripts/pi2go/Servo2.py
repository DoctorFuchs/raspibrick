# Servo2.py
# Servo test

from raspibrick import *

robot = Robot()
servo2 = ServoMotor(2, 300, 2)
servo3 = ServoMotor(3, 300, 2)
Tools.delay(3000)

for pos in range(-50, 55, 10):
    print pos
    servo2.setPos(pos)
    Tools.delay(1000)
servo2.setPos(0)
print "home"

for pos in range(-50, 55, 10):
    print pos
    servo3.setPos(pos)
    Tools.delay(1000)
servo3.setPos(0)
print "home"

print "all done"
robot.exit()
