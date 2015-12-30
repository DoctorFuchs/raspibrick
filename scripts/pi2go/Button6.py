# Button6.py

from raspibrick import *

def onButtonEvent(event):
    global isExiting
    if event == SharedConstants.BUTTON_PRESSED:
        print "pressed"
    elif event == SharedConstants.BUTTON_RELEASED:
        print "released"
    elif event == SharedConstants.BUTTON_CLICKED:
        print "clicked"
    elif event == SharedConstants.BUTTON_DOUBLECLICKED:
        print "double clicked"
    elif event == SharedConstants.BUTTON_LONGPRESSED:
        print "long pressed"
#        isExiting = True


robot = Robot()
#robot.addButtonListener(onButtonEvent)  # no double-click
robot.addButtonListener(onButtonEvent, True)  # enable double-click
#robot.addButtonListener(onButtonEvent, True, 3)  # enable double-click with 3s double click time
print "Started. Press button now..."
isExiting = False
while not isExiting:
    Tools.delay(100)
robot.exit()
print "All done"
