# Display2.py

from raspibrick import *

print "Displayable:", Disp4tronix.getDisplayableChars()
robot = Robot()
display = Display()
k = 32

while k < 128:
    print "<cr> or x<cr> to terminate",
    text = raw_input()	# Fetch the input from the terminal
    if text == "x":
        break
    s = chr(k) + chr(k+1) + chr(k+2) + chr(k+3)
    print k, s
    display.showText(s)
    k += 4

robot.exit()
print "All done"
