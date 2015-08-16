# update-wpa.py

from raspibrick import *

robot = Robot()
led = Led(1)
display = Display()
display.setText("boot")
led.setColor(10, 0, 0)
Tools.delay(2000)
robot.exit()
