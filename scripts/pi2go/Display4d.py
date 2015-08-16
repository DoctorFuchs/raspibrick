# Display4d.py

from raspibrick import *

def onButtonEvent(event):
    global isInterrupted
    if event == BUTTON_PRESSED:
        print "Button pressed"
        isInterrupted = True


robot = Robot()
robot.addButtonListener(onButtonEvent)
n = 0

display = Display()
print "Starting ticker..."
display.ticker("1234567890", 2)
isInterrupted = False
while not isInterrupted and display.isTickerAlive():
    Tools.delay(100)
#    print "n =", str(n)
    n += 1
display.stopTicker()
print "All done."
