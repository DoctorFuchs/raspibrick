# Display4c.py

from raspibrick import *

robot = Robot()
n = 0

display = Display()
print "Starting ticker..."
display.ticker("1234567890", 2, 8, True)
while  display.isTickerAlive():
    print n, "running"
    n += 1
    Tools.delay(100)
robot.exit()
print "All done"
