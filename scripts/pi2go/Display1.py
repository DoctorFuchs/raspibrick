# Display1.py

from raspibrick import *

robot = Robot("192.168.0.2")
display = Display()
for digit in range(4):
    display.setDigit("A", digit)
    Tools.delay(1000)
robot.exit()
