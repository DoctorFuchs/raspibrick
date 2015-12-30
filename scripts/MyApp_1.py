# Demo1.py

from raspibrick import *

robot = Robot()
display = Display()
display.showTicker("Press to end", count = 0)
led = Led(0)
n = 0
while not robot.isButtonHit():
    led.setColor(n, n, n)
    n += 5
    if n == 100:
        n = 0
    Tools.delay(100)
led.setColor(0, 0, 0)
robot.exit()
