# Motor2.py

from raspibrick import *

robot = Robot()
mot = Motor(MOTOR_RIGHT)
mot.forward(3000)
robot.exit()
