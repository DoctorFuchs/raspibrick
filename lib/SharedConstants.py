# SharedConstants.py
# For Py2Go (full model)

'''
Constants and defaults for the RaspiBrick libray based on Pi2Go (full version) from 4tronix.

 This software is part of the raspibrick module.
 It is Open Source Free Software, so you may
 - run the code for any purpose
 - study how the code works and adapt it to your needs
 - integrate all or parts of the code in your own programs
 - redistribute copies of the code
 - improve the code and release your improvements to the public
 However the use of the code is entirely your responsibility.
'''

'''
General remarks:
- Pin definitions start with P_
'''

'''
History:

V1.15 - Sep 2015: - First public release
V1.16 - Oct 2015: - Added: Sensor events
V1.17 - Oct 2015: - Modified: Timeout to receive echo in ultrasonic sensor
V1.18 - Oct 2015: - Fixed: Gear.leftArc(), rightArc() now work with changing radius
'''

VERSION = "1.18 - Oct 2015"
DISPLAYED_VERSION = "118" # displayed n.nn

DEBUG = False

BLINK_CONNECT_DISCONNECT = True

# -------------------- Start of pin definitions ------------------
# Motor pins
P_LEFT_FORWARD = 26
P_LEFT_BACKWARD = 24
P_RIGHT_FORWARD = 19
P_RIGHT_BACKWARD = 21

# Infrared sensor pins
P_FRONT_CENTER = 13
P_FRONT_LEFT = 11
P_FRONT_RIGHT = 7
P_LINE_LEFT = 12
P_LINE_RIGHT = 15

# Pushbutton pin
P_BUTTON = 16

 # Ultrasonic pin
P_TRIG_ECHO = 8

# Battery monitor pin
P_BATTERY_MONITOR = 18
# -------------------- End of pin definitions --------------------

# Motor constants
MOTOR_PWM_FREQ = 30  # PWM frequency (Hz)
LEFT_MOTOR_PWM = [0] * 2  # PWMs
RIGHT_MOTOR_PWM = [0] * 2 # PWMs

# Motor IDs
MOTOR_LEFT = 0
MOTOR_RIGHT = 1

# Infrared IDs
IR_CENTER = 0
IR_LEFT = 1
IR_RIGHT = 2
IR_LINE_LEFT = 3
IR_LINE_RIGHT = 4

# LED IDs
LED_FRONT = 0
LED_LEFT = 1
LED_REAR = 2
LED_RIGHT = 3

# LED and Servo PWM frequency
PWM_FREQ = 50

# Light sensor IDs
LS_FRONT_LEFT = 0
LS_FRONT_RIGHT = 1
LS_REAR_LEFT = 2
LS_REAR_RIGHT = 3

# Servo constants
SERVO_0 = 12  # PCA9685 port, S12 header
SERVO_1 = 13  # PCA9685 port, S13 header
SERVO_2 = 14  # PCA9685 port, S14 header
SERVO_3 = 15  # PCA9685 port, S15 header

# Default speed
MOTOR_DEFAULT_SPEED = 40

# Length of axes used in Gear.leftArc(), Gear.rightArc()
GEAR_AXE_LENGTH = 0.05
# Default speed
GEAR_DEFAULT_SPEED = 30
# Difference between left and right motor in Gear() due to different mechanics
# diff = leftSpeed - rightSpeed
GEAR_FORWARD_SPEED_DIFF = 0.5
GEAR_BACKWARD_SPEED_DIFF = 0.5

BUTTON_PRESSED = 1
BUTTON_RELEASED = 2
BUTTON_LONGPRESSED = 3
BUTTON_LONGPRESS_DURATION = 10 # time (in 200 ms units) the button must be pressed to be a long press

# Character to binary value mapping for 4 digit 7 segment display
PATTERN = {'A':119, 'b':124, 'C':57, 'd':94, 'E':121, 'F':113,
            '0':63, '1':6, '2':91, '3':79, '4':102, '5':109, '6':125, '7':7, '8':127, '9':111,
           '-':64, 'c':88, 'O':63, 'C':57, 'H':118,'I':48, 'J':30,'L':56, 't':120, 'U':62, 'u':28, 'r':80, 'P':115,
           'n':84, 'o':92, 'i':16, 'Y':110, ' ':0, '|':73, '=':72, '%':54}

# Event poll delay (ms)
POLL_DELAY = 50

ABOUT = "2003-2015 Aegidius Pluess\n" + \
         "OpenSource Free Software\n" + \
         "http://www.aplu.ch\n" + \
         "All rights reserved"

