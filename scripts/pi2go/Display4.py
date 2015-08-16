# Display4.py

from raspibrick import *

robot = Robot()
n = 0

display = Display()
print "Starting ticker..."
display.ticker("1234567890")
while  display.isTickerAlive():
    print n, "running"
    n += 1
    Tools.delay(100)
print "finished"
Tools.delay(2000)
robot.exit()
print "All done"
