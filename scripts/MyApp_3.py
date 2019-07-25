# Demo3.py

from raspibrick import *

def show(d):
    v = str(d)
    v = v.replace(".", "")
    v = " " + v
    display.showText(v)
    
robot = Robot()
gear = Gear()
us = UltrasonicSensor()
display = Display()
gear.setSpeed(15)
display.showText("HAnd")
Tools.delay(3000)
gear.forward()

while not isEscapeHit():
    d = us.getValue()
    show(d)
    if d < 19:
        gear.backward()
    elif d > 21:
        gear.forward() 
    else:
        gear.stop()  
robot.exit()