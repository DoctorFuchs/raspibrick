# Motor3.py

from raspibrick import *

robot = Robot()
mot1 = Motor(MOTOR_LEFT)
mot2 = Motor(MOTOR_RIGHT)
mot1.backward()
mot2.backward()
Tools.delay(3000)
robot.exit()
print "All done"
