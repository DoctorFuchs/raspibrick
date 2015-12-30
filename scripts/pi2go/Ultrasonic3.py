# Ultrasonic3.py

from raspibrick import *

robot = Robot()
uss = UltrasonicSensor()
display = Display()

while not isEscapeHit():
    v = str(uss.getValue())
    v = v.replace(".", "")
    v = " " + v
    display.setText(v, [1, 0, 0])
    Tools.delay(1000)
robot.exit()
