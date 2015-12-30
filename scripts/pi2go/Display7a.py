# Display7a.py
# Blinker test, ctor params


from raspibrick import *

robot = Robot()
dp = Display()
text = "boot"
dp.showBlinker(text, dp = [0, 1, 0], count = 4, speed = 2, blocking = True)
robot.exit()
print "all done"
