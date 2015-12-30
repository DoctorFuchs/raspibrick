# Sound4.py

from raspibrick import *

robot = Robot()
robot.initSound("/home/pi/salza1.wav", 50)
robot.playSound()
while robot.isSoundPlaying():
    print "playing"
    Tools.delay(1000)

print "All done"
