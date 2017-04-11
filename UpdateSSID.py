# UpdateSSID.py

from raspibrick import *

robot = Robot()
if robot.oled != None:
    text = "SSID update request."
    robot.oled.setText(text, 0, 12, 0)
    text = "Must reboot now..."
    robot.oled.setText(text, 2, 12, 0)
else:
    display = Display()
    display.showTicker("  SSID UPdAtE", 1, 1, True)
    display.showBlinker("boot", [0], 2, 1)
led = Led(1)
led.setColor(10, 0, 0)
Tools.delay(3000)
if robot.oled != None:
    robot.oled.clear()
robot.exit()
