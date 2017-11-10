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
V1.19 - Oct 2015: - Added: Led.setColor(), setColorAll() with X11-color string
V1.20 - Oct 2015: - Modifications to RaspiJLib
V1.21 - Oct 2015: - Added: ButtonListener with long press event
V1.22 - Nov 2015: - Added: Class DgTell, Button click and double-click events
V1.23 - Dec 2015: - Added: Selecting up to 9 autonomous Python programs
V1.24 - Dec 2015: - Modified: Shutdown confirmation with button press event
V1.25 - Dec 2015: - Modified: Decimal point display for DgTell
V1.26 - Jan 2016: - Added: tcpcom.py Event driven socket library
V1.28 - Feb 2016: - Fixed: Inhibit repeat same text in Display
V1.29 - Mar 2016: - Added: Escape into SELF/AUTO mode
V1.30 - Mar 2016: - Changed SELF mode to use buzzer/led to show IP
V1.31 - Apr 2016: - Fixed: startApp now checks standalone or Pi2Go mode
                  - Fixed: Error in Ultrasonic.py reporting too large distance
V1.32 - May 2016: - New Linux installations: SoX, DHT driver from Adafruit, 1-Wire driver (kernel)
V1.33 - May 2016: - Patched Scratch image to avoid popup dialog when remote sensor is enabled,
                  - Screen blanking for console disabled
                  - Login shell over serial disabled (in raspi-config)
                  - OLED driver Adafruit_Python_SSD1306
V1.34 - Jun 2016: - startApp modified to accept fully qualified path to script
V1.35 - Oct 2016: - Geany, PyQT4 installed, new sudirectory rpi-tutorial, 
                    in Pictures: einstein.ppm
V1.36 - Apr 2017: - Updates: RaspiBrick libraries, TigerJython
                  - Morse announcement removed in Pi2Go startup
                  - Support for OLED display in Pi2Go mode
                  - Bluetooth server no longer started at boot time
                  - Adapted to new NOOPs release
V1.37 - May 2017: - OLED1306 thread-safe now
V1.38 - Nov 2017: - Added: TM1637.py
'''

VERSION = "1.38 - Nov 2017"
DISPLAYED_VERSION = "138"  # displayed n.nn

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
PWM_I2C_ADDRESS = 0x40
# LED and Servo PWM frequency
PWM_FREQ = 50

# ADC I2C address
ADC_I2C_ADDRESS = 0x48

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

# Button event constants
BUTTON_PRESSED = 1
BUTTON_RELEASED = 2
BUTTON_LONGPRESSED = 3
BUTTON_CLICKED = 4
BUTTON_DOUBLECLICKED = 5
BUTTON_LONGPRESS_DURATION = 2 # time (in s) the button must be pressed to be a long press
BUTTON_DOUBLECLICK_TIME = 1 # default time (in s) to wait for a double click event

# Character to binary value mapping for 4 digit 7 segment display
PATTERN = {' ': 0, '!': 134, '"': 34, '#': 0, '$': 0, '%': 0, '&': 0, '\'':  2, '(': 0, ')': 0,
           '*': 0, '+': 0, ',': 4, '-': 64, '.': 128, '/': 82, '0': 63, '1': 6, '2': 91, '3': 79,
           '4': 102, '5': 109, '6': 125, '7': 7, '8': 127, '9': 111, ':': 0, ';': 0, '<': 0,
           '=': 72, '>': 0, '?': 0, '@': 93, 'A': 119, 'B': 124, 'C': 88, 'D': 94, 'E': 121,
           'F': 113, 'G': 61, 'H': 118, 'I': 48, 'J': 14, 'K': 112, 'L': 56, 'M': 85, 'N': 84,
           'O': 63, 'P': 115, 'Q': 103, 'R': 80, 'S': 45, 'T': 120, 'U': 62, 'V': 54, 'W': 106,
           'X': 73, 'Y': 110, 'Z': 27, '[': 57, '\\':  100, ']': 15, '^': 35, '_': 8, '`': 32,
           'a': 119, 'b': 124, 'c': 88, 'd': 94, 'e': 121, 'f': 113, 'g': 61, 'h': 116, 'i': 16,
           'j': 12, 'k': 112, 'l': 48, 'm': 85, 'n': 84, 'o': 92, 'p': 115, 'q': 103, 'r': 80, 's': 45,
           't': 120, 'u': 28, 'v': 54, 'w': 106, 'x': 73, 'y': 110, 'z': 27, '{': 0, '|': 48, '}': 0, '~': 65}

# Config file to store last program name
CONFIG_FILE = "/home/pi/scripts/raspibrick.cfg"
# Path of execution app
APP_PATH = "/home/pi/scripts/MyApp"

# Event poll delay (ms)
POLL_DELAY = 50

ABOUT = "2003-2016 Aegidius Pluess\n" + \
         "OpenSource Free Software\n" + \
         "http://www.aplu.ch\n" + \
         "All rights reserved"

