# Button1.py

import RPi.GPIO as GPIO
import time

# Button pin
pin = 16

print "starting"
GPIO.setmode(GPIO.BOARD) # Use physical pin numbers
GPIO.setwarnings(False)

GPIO.setup(pin, GPIO.IN, GPIO.PUD_UP)
while True:
    if GPIO.input(pin) == GPIO.HIGH:
        print "Hi"
    else:
        print "Lo"
    time.sleep(0.1)
