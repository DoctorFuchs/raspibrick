# ButtonLib.py

import RPi.GPIO as GPIO
import time
from threading import Thread

DEBUG = False

# Button event constants
BUTTON_PRESSED = 1
BUTTON_RELEASED = 2
BUTTON_LONGPRESSED = 3
BUTTON_CLICKED = 4
BUTTON_DOUBLECLICKED = 5
BUTTON_LONGPRESS_DURATION = 2 # default (in s) the button must be pressed to be a long press
BUTTON_DOUBLECLICK_TIME = 1 # default time (in s) to wait for a double click event

def delay(interval):
    time.sleep(interval / 1000.0)

class ClickThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.start()

    def run(self):
        if DEBUG:
            print("===>ClickThread started")
        global clickThread
        self.isRunning = True
        startTime = time.time()
        while self.isRunning and (time.time() - startTime < BUTTON_DOUBLECLICK_TIME):
            time.sleep(0.1)
        if clickCount == 1 and not isLongPressEvent:
            if xButtonListener != None:
                xButtonListener(BUTTON_CLICKED)
            clickThread = None
        self.isRunning  = False
        if DEBUG:
            print("===>ClickThread terminated")

    def stop(self):
        self.isRunning = False

class ButtonThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.isRunning = False

    def run(self):
        if DEBUG:
            print("===>ButtonThread started")
        self.isRunning = True
        startTime = time.time()
        while self.isRunning and (time.time() - startTime < BUTTON_LONGPRESS_DURATION):
            time.sleep(0.1)
        if self.isRunning:
            if buttonListener != None:
                buttonListener(BUTTON_LONGPRESSED)
        if DEBUG:
            print("===>ButtonThread terminated")

    def stop(self):
        self.isRunning = False

def onXButtonEvent(event):
    global clickThread, clickCount, isLongPressEvent
    if event == BUTTON_PRESSED:
        if xButtonListener != None:
            xButtonListener(BUTTON_PRESSED)
        isLongPressEvent = False
        if clickThread == None:
            clickCount = 0
            clickThread = ClickThread()

    elif event == BUTTON_RELEASED:
        if xButtonListener != None:
            xButtonListener(BUTTON_RELEASED)
        if isLongPressEvent and clickThread != None:
            clickThread.stop()
            clickThread = None
            return
        if clickThread != None and clickThread.isRunning:
            clickCount += 1
            if clickCount == 2:
                clickThread.stop()
                clickThread = None
                if xButtonListener != None:
                    xButtonListener(BUTTON_DOUBLECLICKED)
        else:
            clickThread = None

    elif event == BUTTON_LONGPRESSED:
        isLongPressEvent = True
        if xButtonListener != None:
            xButtonListener(BUTTON_LONGPRESSED)

# Hardware callback
def onButtonEvent(channel):
    global buttonThread, inCallback
    if inCallback: # inhibit reentrance
        return
    inCallback = True
    # switch may bounce: down-up-up, down-up-down, down-down-up etc. in fast sequence
    if GPIO.input(buttonPin) == GPIO.LOW:
        if buttonThread == None: # down-down is suppressed
            if DEBUG:
                print("->ButtonDown")
            buttonThread = ButtonThread()
            buttonThread.start()
            if buttonListener != None:
                buttonListener(BUTTON_PRESSED)
    else:
        if buttonThread != None: # up-up is suppressed
            if DEBUG:
                print("->ButtonUp")
            buttonThread.stop()
            buttonThread.join(200) # wait until finished
            buttonThread = None
            if buttonListener != None:
                buttonListener(BUTTON_RELEASED)
    inCallback = False
    
def addXButtonListener(listener):
    global xButtonListener
    addButtonListener(onXButtonEvent)
    xButtonListener = listener

def addButtonListener(listener):
    global buttonListener
    buttonListener = listener

def setButtonPin(pin):
    global buttonPin
    buttonPin = pin
    GPIO.setup(buttonPin, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(buttonPin, GPIO.BOTH, onButtonEvent)

buttonThread = None
clickThread = None
inCallback = False

# Use physical pin numbers
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

