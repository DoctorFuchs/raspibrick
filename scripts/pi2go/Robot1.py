# Robot1.py

from raspibrick import *

version = Robot.getVersion()
print "BrickGate Version:", version
ipAddresses = Robot.getIPAddresses()
print "IP address:", ipAddresses
print "All done"
