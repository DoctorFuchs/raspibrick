# IRSensor1.py

from raspibrick import *

robot = Robot()
ir_left = InfraredSensor(IR_LINE_LEFT)

while not isEscapeHit():
    v = ir_left.getValue()
    print "v:", v
    Tools.delay(1000)
robot.exit()
