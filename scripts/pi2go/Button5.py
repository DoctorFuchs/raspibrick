# Button5.py

from raspibrick import *
from threading import Thread
import time

class ClickThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.start()

    def run(self):
        global clickThread
        print "ClickThread running"
        self.isRunning = True
        startTime = time.time()
        while self.isRunning and (time.time() - startTime < doubleClickTime):
            time.sleep(0.01)
        if clickCount == 1 and not isLongPressEvent:
            print "--------------Click Event"
            clickThread = None
        self.isRunning  = False
        print "ClickThread terminated"

    def stop(self):
        self.isRunning = False

def onButtonEvent(event):
    global clickThread, clickCount, isLongPressEvent
    if event == SharedConstants.BUTTON_PRESSED:
        print "----------------Press Event"
        isLongPressEvent = False
        if clickThread == None:
            clickCount = 0
            print "clickCount init to 0"
            clickThread = ClickThread()

    elif event == SharedConstants.BUTTON_RELEASED:
        print "----------------Release Event"
        if isLongPressEvent:
            clickThread.stop()
            clickThread = None
            return
        if clickThread.isRunning:
            clickCount += 1
            print "clickCount:", clickCount
            if clickCount == 2:
                clickThread.stop()
                clickThread = None
                print "--------------Double-Click Event"
        else:
            clickThread = None

    elif event == SharedConstants.BUTTON_LONGPRESSED:
        isLongPressEvent = True
        print "--------------Long-Press Event"

doubleClickTime = 1
robot = Robot()
robot.addButtonListener(onButtonEvent)
clickThread = None
print "Started. Press button now..."
while True:
    Tools.delay(100)
robot.exit()
print "All done"
