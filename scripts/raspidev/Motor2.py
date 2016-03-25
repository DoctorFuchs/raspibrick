# Motor2.py
# Leds/Motor at pin 19/21

import RPi.GPIO as GPIO
import time

# LED/Motor pins
pin1 = 19
pin2 = 21

pwmFrequency = 50  # Hz

print "starting"

# Use physical pin numbers
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Right motor
GPIO.setup(pin1, GPIO.OUT)
pwm1 = GPIO.PWM(pin1, pwmFrequency)
pwm1.start(0)
GPIO.setup(pin2, GPIO.OUT)
pwm2 = GPIO.PWM(pin2, pwmFrequency)
pwm2.start(0)

print "right forward"
pwm2.ChangeDutyCycle(0)
for duty in range(0, 101, 10):
    print "duty:", duty
    pwm1.ChangeDutyCycle(duty)
    time.sleep(2)

print "backward"
pwm1.ChangeDutyCycle(0)
for duty in range(0, 101, 10):
    print "duty:", duty
    pwm2.ChangeDutyCycle(duty)
    time.sleep(2)
print "all done"