# Robot1.py

from raspibrick import *

robot = Robot()
version = robot.getBrickgateVersion()
print "Brickgate Version:", version
ipAddress = robot.getIPAddress()
print "IP address:", ipAddress
gear = Gear()
devices = robot.getCurrentDevices()
print "Current devices:", devices
Tools.delay(4000)
robot.exit()
