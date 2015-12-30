# UpdateSSID.py

from raspibrick import *

robot = Robot()
led = Led(1)
display = Display()
display.showTicker("  SSID UPdAtE", 1, 1, True)
display.showBlinker("boot", [0], 2, 1)
led.setColor(10, 0, 0)
Tools.delay(2000)
robot.exit()
