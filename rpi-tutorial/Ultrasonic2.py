# Ultrasonic2.py
# Show distance on Oled

import RPi.GPIO as GPIO
import time
from OLED1306 import OLED1306

P_ESCAPE = 12 # Button A
P_TRIGGER = 15
P_ECHO = 16

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(P_TRIGGER, GPIO.OUT)
    GPIO.setup(P_ECHO, GPIO.IN)
    GPIO.setup(P_ESCAPE, GPIO.IN)

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
oled = OLED1306()
oled.setFontSize(50)
setup()
while GPIO.input(P_ESCAPE) == GPIO.LOW:
    d = getDistance()
    oled.setText(str(d))
    time.sleep(1)
GPIO.cleanup()
oled.setText("done")
    

