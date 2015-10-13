# IdleProcess.py

import sys
from threading import Thread

from raspibrick import *


def onButtonEvent(event):
    global rc, isAlive, shutdown, isShutdownPending, isShutdownCanceled, isInterrupted
    isInterrupted = True
    if not isAlive:
        return
    if event == BUTTON_PRESSED:
        print "Button pressed"
        if isShutdownPending:
            if ir_center.getValue() == 1:
               shutdown = True
               rc = 3
               isAlive = False
            else:
                isShutdownPending = False
                led.setColor(0, 0, 100)
                display.setText("1dLE")
                isShutdownCanceled = True
    elif event == BUTTON_LONGPRESSED:
        print "Button long pressed"
        if ir_center.getValue() == 1:
            if not isShutdownPending:
                isShutdownPending = True
                isShutdownCanceled = False
                display.setText("oooo")
                led.setColor(100, 0, 0)
        else:
            isShutdownPending = False
            rc = 2
            isAlive = False
    elif event == BUTTON_RELEASED:
        print "Button released"
        if isShutdownPending or isShutdownCanceled:
            isShutdownCanceled = False
            return
        rc = 1
        isAlive = False

def firstDuty():
    display.setText("E" + SharedConstants.DISPLAYED_VERSION, [0, 1, 0])
    Tools.delay(4000)
    display.setText("AP--")
    count = 0
    ip = ""
    robot.setButtonEnabled(True)
    while not isInterrupted and count < 40:  # Try 20 s to get IP address
       ipAddr = robot.getIPAddresses()
       print "Got IP addresses:", ipAddr
       ip = ""
       for addr in ipAddr:
           if addr != '127.0.0.1':
              ip += "|"
              ip += addr
              ip += "    "
       if ip != "":
           break
       count += 1
       Tools.delay(500)
    display.clear()
    if ip == "":
        led.setColor(10, 10, 0)
    else:
        led.setColor(0, 20, 0)
    if display.isAvailable():
        if not isInterrupted and display.isAvailable():
            if ip == "":
                ip = "|0.0.0.0    "
            ip = ip.replace(".", "-")
            display.ticker(ip, 3, 1)
            while not isInterrupted and display.isTickerAlive():
                Tools.delay(1000)
            display.stopTicker()
    else:
        Tools.delay(3000)

print "IdleProcess starting"
rc = 0
robot = Robot()
display = Display()
led = Led(LED_LEFT)
led.setColor(10, 10, 10) # Announce, we are starting
robot.setButtonEnabled(False)
robot.addButtonListener(onButtonEvent)
isInterrupted = False

if sys.argv[1] == "isFirst":
    firstDuty()
else:
    robot.setButtonEnabled(True)

isAlive = True
led.setColor(0, 0, 50) # Announce, we are running
display.setText("1dLE")
ir_center = InfraredSensor(IR_CENTER)
isShutdownPending = False
isShutdownCanceled = False
while isAlive:
    Tools.delay(1000)
display.clear()
led.setColor(0, 0, 0)
Tools.delay(1000)
print "Returning to parent process with rc:", rc
sys.exit(rc)



