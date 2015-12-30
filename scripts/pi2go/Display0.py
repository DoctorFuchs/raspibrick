# Display0.py

from raspibrick import *

print "Creating robot"
robot = Robot()
print "Creating display"
display = Display()
Tools.delay(3000)
print "exit"
robot.exit()
print "All done"
