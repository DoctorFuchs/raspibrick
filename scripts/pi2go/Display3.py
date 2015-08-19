# Display3.py

from raspibrick import *

robot = Robot()
display = Display()
display.setScrollableText("123-456-789-AbC")
while not isEscapeHit():
    Tools.delay(700)
    rc = display.scrollToLeft()
    print rc
    if rc == 4:
        Tools.delay(1500)
        display.setText("")
        Tools.delay(1500)
        display.setToStart()
Tools.delay(2000)
robot.exit()
