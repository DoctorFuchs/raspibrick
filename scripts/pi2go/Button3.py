# Button3.py

from raspibrick import *

def onButtonEvent(event):
    global n
    if event == SharedConstants.BUTTON_PRESSED:
        print "pressed"
    elif event == SharedConstants.BUTTON_RELEASED:
        print "released"
    elif event == SharedConstants.BUTTON_LONGPRESSED:
        print "long pressed"
        n += 1
    print "n", n

robot = Robot()
robot.addButtonListener(onButtonEvent)
n = 0
while n < 4:
    Tools.delay(100)
robot.exit()
print "All done"
