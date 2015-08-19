# Display4.py

from raspibrick import *

robot = Robot()

display = Display()
display.ticker("1234567890")
#robot.ticker("1234567890", 2)
#display.ticker("1234567890", 2, 8)
count = 0;
while display.isTickerAlive():
    print "alive at", count
    count +=1
    Tools.delay(500)

robot.exit()
print "All done"
