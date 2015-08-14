import RPi.GPIO as GPIO
import time
import sys
from xsgh_PCF8591P import sgh_PCF8591P


# I2C analog extender chip
print "Trying to detect PCF8591 I2C analog extender on I2C bus 0..."
try:
    analogExtender = sgh_PCF8591P(0) # i2c at address 0x48
    print "PCF8591 I2C analog extender on I2C bus # 0 detected"
except:
    print "Failed, trying with bus number 1..."
    try:
        analogExtender = sgh_PCF8591P(1) # i2c at address 0x48
        print "PCF8591 I2C analog extender on I2C bus # 1 detected"
    except:
        print "Failed to detect PCF8591 I2C analog extender on I2C bus"
        sys.exit(1)

for n in range(100):
    print n, ":",
    for nb in range(4):
        v = analogExtender.readADC(nb)
        print nb, "->", v,
    print ""
    time.sleep(1)
