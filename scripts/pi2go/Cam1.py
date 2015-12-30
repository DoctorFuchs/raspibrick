# Cam1.py

from raspibrick import *

robot = Robot()
print "Capturing image..."
camera = Camera()
img = camera.captureJPEG(300, 200)
print "size", len(img)
camera.saveData(img, "/home/pi/test.jpg")
robot.exit()
