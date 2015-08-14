import RPi.GPIO as GPIO
import time

# Infrared sensor pins
P_FRONT_CENTER = 13
P_FRONT_LEFT = 11
P_FRONT_RIGHT = 7
P_LINE_LEFT = 12
P_LINE_RIGHT = 15

# Use physical pin numbers
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# IR sensors
GPIO.setup(P_FRONT_LEFT, GPIO.IN)
GPIO.setup(P_FRONT_CENTER, GPIO.IN)
GPIO.setup(P_FRONT_RIGHT, GPIO.IN)
GPIO.setup(P_LINE_LEFT, GPIO.IN)
GPIO.setup(P_LINE_RIGHT, GPIO.IN)

for n in range(100):
    v_front_left = GPIO.input(P_FRONT_LEFT)
    v_front_center = GPIO.input(P_FRONT_CENTER)
    v_front_right = GPIO.input(P_FRONT_RIGHT)
    v_line_left = GPIO.input(P_LINE_LEFT)
    v_line_right = GPIO.input(P_LINE_RIGHT)
    print n
    print "FRONT_LEFT:", v_front_left, \
        "FRONT_CENTER:", v_front_center, \
        "FRONT_RIGHT", v_front_right, \
        "LINE_LEFT", v_line_left, \
        "LINE_RIGHT", v_line_right
    time.sleep(1)
