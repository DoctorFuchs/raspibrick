# LED1.py
from raspibrick import *

robot = Robot()
Led.setColorAll(100, 0, 0)
while not isEscapeHit():
    continue
robot.exit()
