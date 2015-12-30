# Cam1a.py

from raspibrick import *

robot = Robot()
print "Capturing image..."
camera = Camera()
camera.captureAndSave(300, 200, "/home/pi/test.jpg")
robot.exit()
