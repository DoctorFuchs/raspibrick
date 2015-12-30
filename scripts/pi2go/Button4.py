# Button4.py

from raspibrick import *

def turnOn(n):
    Led.clearAll()
    leds[n].setColor("white")

def onButtonEvent(event):
    global isRunning, z
    if event == SharedConstants.BUTTON_PRESSED:
        z  = (z + 1) % 4
        turnOn(z)
    elif event == SharedConstants.BUTTON_LONGPRESSED:
        isRunning = False

robot = Robot(buttonEvent = onButtonEvent)
# robot.addButtonListener(onButtonEvent)
leds = [0] * 4
for n in range(4):
    leds[n] = Led(n)

leds[0].setColor("green")
z = 0
isRunning = True
while isRunning:
    Tools.delay(100)
Led.setColorAll("red")
Tools.delay(2000)
robot.exit()
