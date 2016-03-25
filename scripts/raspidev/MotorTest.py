# Motor1.py

import RPi.GPIO as GPIO
import time

# Motor pins
P_LEFT_FORWARD = 26
P_LEFT_BACKWARD = 24
P_RIGHT_FORWARD = 19
P_RIGHT_BACKWARD = 21

MOTOR_PWM_FREQ = 30  # PWM frequency (Hz)

# Use physical pin numbers
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Left motor
GPIO.setup(P_LEFT_FORWARD, GPIO.OUT)
pwm_left_forward = GPIO.PWM(P_LEFT_FORWARD, MOTOR_PWM_FREQ)
pwm_left_forward.start(0)
GPIO.setup(P_LEFT_BACKWARD, GPIO.OUT)
pwm_left_backward = GPIO.PWM(P_LEFT_BACKWARD, MOTOR_PWM_FREQ)
pwm_left_backward.start(0)

# Right motor
GPIO.setup(P_RIGHT_FORWARD, GPIO.OUT)
pwm_right_forward = GPIO.PWM(P_RIGHT_FORWARD, MOTOR_PWM_FREQ)
pwm_right_forward.start(0)
GPIO.setup(P_RIGHT_BACKWARD, GPIO.OUT)
pwm_right_backward = GPIO.PWM(P_RIGHT_BACKWARD, MOTOR_PWM_FREQ)
pwm_right_backward.start(0)

print "left forward"
pwm_left_forward.ChangeDutyCycle(50);
time.sleep(3)
print "stop"
pwm_left_forward.ChangeDutyCycle(0);
time.sleep(1)

print "left backward"
pwm_left_backward.ChangeDutyCycle(50);
time.sleep(3)
print "stop"
pwm_left_backward.ChangeDutyCycle(0);
time.sleep(1)

print "right forward"
pwm_right_forward.ChangeDutyCycle(50);
time.sleep(3)
print "stop"
pwm_right_forward.ChangeDutyCycle(0);
time.sleep(1)

print "right backward"
pwm_right_backward.ChangeDutyCycle(50);
time.sleep(3)
print "stop"
pwm_right_backward.ChangeDutyCycle(0);
time.sleep(1)

print "All done"


