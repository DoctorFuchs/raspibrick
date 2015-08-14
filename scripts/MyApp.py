# MyApp.py

from raspibrick import *

print "MyApp running"
robot = Robot()
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
