# ResetLED.py

from raspibrick import *
import RPi.GPIO as GPIO

robot = Robot()
Led.clearAll()
robot.exit()
GPIO.cleanup()
print("Reset done")

