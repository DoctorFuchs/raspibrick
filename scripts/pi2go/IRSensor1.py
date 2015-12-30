# IRSensor1.py

from raspibrick import *

robot = Robot()
ir_left = InfraredSensor(IR_LEFT)
ir_center = InfraredSensor(IR_CENTER)
ir_right = InfraredSensor(IR_RIGHT)
ir_line_left = InfraredSensor(IR_LINE_LEFT)
ir_line_right = InfraredSensor(IR_LINE_RIGHT)

while not isEscapeHit():
    v_left = ir_left.getValue()
    v_right = ir_right.getValue()
    v_center = ir_center.getValue()
    v_line_left = ir_line_left.getValue()
    v_line_right = ir_line_right.getValue()
    print "left:", v_left, "center:", v_center, "right:", v_right, \
        "line_left:", v_line_left, "line_right:", v_line_right
    Tools.delay(1000)
robot.exit()
print "All done"