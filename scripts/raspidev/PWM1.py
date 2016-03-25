# PWM1.py
# Servo motor driven by PCA9685 chip
# duty = 0..4096  (0, 4096: all low)
# remain state even when program ends

from smbus import SMBus
from PCA9685Lib import PWM

i2c_address = 0x40
pwm_frequency = 50
channel = 0

print "starting"
bus = SMBus(1) # For revision 2 Raspberry Pi
pwm = PWM(bus, i2c_address)
pwm.setFreq(pwm_frequency)
duty = 1024
pwm.setDuty(channel, duty)
print "all done"
