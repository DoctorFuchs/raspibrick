# IRSensor1a.py
# Events

from raspibrick import *

def onActivated(id):
    print "activate event at", id

def onPassivated(id):
    print "passivate event", id

robot = Robot()
irs = InfraredSensor(IR_CENTER, activated = onActivated, passivated = onPassivated)

while not isEscapeHit():
    Tools.delay(100)
robot.exit()
print "All done"