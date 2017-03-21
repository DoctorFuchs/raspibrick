# Ultrasonic1.py
# Using HC-SR04 ultrasonic module

import RPi.GPIO as GPIO
import time

P_TRIGGER = 15
P_ECHO = 16

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(P_TRIGGER, GPIO.OUT)
    GPIO.setup(P_ECHO, GPIO.IN)

def getDistance(timeoutCount  = 10000):        
    # Send max 10 us trigger pulse
    GPIO.output(P_TRIGGER, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(P_TRIGGER, GPIO.LOW)
    # Wait for HIGH signal
    count1 = 0
    while GPIO.input(P_ECHO) == GPIO.LOW and count1 < timeoutCount:
        count1 += 1
    startTime = time.time()    
    # Wait for LOW signal
    count2 = 0
    while GPIO.input(P_ECHO) == GPIO.HIGH and count2 < timeoutCount:
        count2 += 1
    if count1 == timeoutCount or count2  == timeoutCount:
        return -1
    elapsed = time.time() - startTime
    distance =  34300 * elapsed / 2.0
    # round to 2 decimals
    distance = int(distance * 100 + 0.5) / 100.0
    return distance

print "starting..."
setup()
while True:
    d = getDistance()
    print "d =", d
    time.sleep(0.1)
    

