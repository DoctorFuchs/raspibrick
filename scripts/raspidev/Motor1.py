# Motor1.py
# Leds/Motor at pin 19/21

import RPi.GPIO as GPIO
import time

# LED/Motor pins
pin1 = 19
pin2 = 21

print "starting"

# Use physical pin numbers
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)
while True:
    GPIO.output(pin1, GPIO.HIGH)
    GPIO.output(pin2, GPIO.LOW)
    time.sleep(0.2)
    GPIO.output(pin1, GPIO.LOW)
    GPIO.output(pin2, GPIO.HIGH)
    time.sleep(0.2)
