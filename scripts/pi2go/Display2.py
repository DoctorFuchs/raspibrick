# Display2.py

from raspibrick import *

robot = Robot()
display = Display()
display.setText("1234")
Tools.delay(4000)
display.setText("1133", [0, 1, 1])
Tools.delay(3000)
display.setText(2244, [0, 1, 1])
Tools.delay(3000)
display.setText("0123456", [0, 0, 0], 2000)
Tools.delay(5000)
robot.exit()
print "All done"
