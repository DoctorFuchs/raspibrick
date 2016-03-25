# Button2.py
# Uses ButtonLib

from ButtonLib import *

def myXButtonListener(event):
    global isExiting
    if event == BUTTON_PRESSED:
        print "pressed"
    elif event == BUTTON_RELEASED:
        print "released"
    elif event == BUTTON_CLICKED:
        print "clicked"
    elif event == BUTTON_DOUBLECLICKED:
        print "double clicked"
    elif event == BUTTON_LONGPRESSED:
        print "long pressed"
        isExiting = True

print "starting"
addXButtonListener(myXButtonListener)
isExiting = False
while not isExiting:
    delay(100)
print "all done"