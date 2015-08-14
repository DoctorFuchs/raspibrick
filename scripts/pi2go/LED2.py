# LED2.py

from raspibrick import *

robot = Robot()
Led.setColorAll(128, 0, 0)
Tools.delay(3000)
Led.setColorAll([128, 128, 0])
Tools.delay(3000)
Led.clearAll()
Tools.delay(3000)
Led.setColorAll(128, 128, 128)
Tools.delay(3000)
robot.exit()
print "All done"