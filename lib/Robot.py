# Robot.py

'''
Abstraction of a robot based on Pi2Go (full version) from 4tronix.

 This software is part of the raspibrick module.
 It is Open Source Free Software, so you may
 - run the code for any purpose
 - study how the code works and adapt it to your needs
 - integrate all or parts of the code in your own programs
 - redistribute copies of the code
 - improve the code and release your improvements to the public
 However the use of the code is entirely your responsibility.
 '''


from RobotInstance import RobotInstance
import RPi.GPIO as GPIO
import os, sys
from Tools import Tools
import SharedConstants
from Display import Display
from Led import Led
from Adafruit_PWM_Servo_Driver import PWM
from sgh_PCF8591P import sgh_PCF8591P
from threading import Thread
from subprocess import Popen, PIPE
import re
import smbus
import socket
import fcntl
import struct

class ButtonThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.isRunning = True

    def run(self):
        count = 0
        while self.isRunning and count < SharedConstants.BUTTON_LONGPRESS_DURATION:
            Tools.delay(200)
            count += 1
        if self.isRunning:
            if _buttonListener != None:
                _buttonListener(SharedConstants.BUTTON_LONGPRESSED)

    def stop(self):
        global _buttonThread
        self.isRunning = False
        _buttonThread = None

def _onButtonEvent(channel):
    if not _isButtonEnabled:
        Tools.debug("Button event detected, but button disabled")
        return
    global _isBtnHit
    global _buttonThread
    try:
        if GPIO.input(SharedConstants.P_BUTTON) == GPIO.LOW:
            Tools.debug("ButtonDown event on channel " + str(channel))
            _isBtnHit = True
            _buttonThread = ButtonThread()
            _buttonThread.start()
            if _buttonListener != None:
                _buttonListener(SharedConstants.BUTTON_PRESSED)
        else:
            Tools.debug("ButtonUp event on channel " + str(channel))
            if _buttonThread != None:
                _buttonThread.stop()
                if _buttonListener != None:
                    _buttonListener(SharedConstants.BUTTON_RELEASED)
    except:  # NoneType error when program is already terminated
        pass

def _onBatteryDown(channel):
    Tools.debug("onBatteryDown event on channel " + str(channel))
    if _batteryListener != None:
        _batteryListener()

_buttonThread = None
_buttonListener = None
_batteryListener = None
_isBtnHit = False
_isButtonEnabled = False

# ------------------------   Class Robot   -------------------------------------------------
class Robot(object):
    '''
    Class that creates or returns a single MyRobot instance.
    '''
    def __new__(cls, *args):
        global _isBtnHit
        if RobotInstance.getRobot() == None:
            r = MyRobot(*args)
            r.isEscapeHit()  # Dummy to clear button hit flag
            RobotInstance.setRobot(r)
            return r
        else:
            r = RobotInstance.getRobot()
            r.isEscapeHit()  # Dummy to clear button hit flag
            return RobotInstance.getRobot()

    @staticmethod
    def getVersion():
        '''
        @return: the module library version
        '''
        return SharedConstants.VERSION

    @staticmethod
    def setSoundVolume(volume):
        '''
        Sets the sound volume. Value is kept when the program exits.
        @param volume: the volume in percent
        '''
        os.system("amixer sset PCM,0 " + str(volume)+ "%  >/dev/null")

    @staticmethod
    def playTone(frequency, duration):
        '''
        Plays a single sine tone with given frequency and duration.
        @param frequency: the frequency in Hz
        @param duration:  the duration in ms
        '''
        os.system("speaker-test -t sine -f " + str(frequency)
                  + " >/dev/null & pid=$! ; sleep " + str(duration / 1000.0) + "s ; kill -9 $pid")

    @staticmethod
    def getIPAddresses():
        '''
        @return:  List of all IP addresses of machine
        '''
        p = Popen(["ifconfig"], stdout = PIPE)
        ifc_resp = p.communicate()
        patt = re.compile(r'inet\s*\w*\S*:\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        resp = patt.findall(ifc_resp[0])
        return resp

# ------------------------   Class MyRobot   -----------------------------------------------
class MyRobot(object):
    '''
    Singleton class that represents a robot.
    '''
    _myInstance = None
    def __init__(self, *args):
        '''
        Creates an instance of MyRobot and initalizes the GPIO.
        '''
        if MyRobot._myInstance != None:
            raise Exception("Only one instance of MyRobot allowed")
        global _isButtonEnabled

        # Use physical pin numbers
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        # Left motor
        GPIO.setup(SharedConstants.P_LEFT_FORWARD, GPIO.OUT)
        SharedConstants.LEFT_MOTOR_PWM[0] = GPIO.PWM(SharedConstants.P_LEFT_FORWARD, SharedConstants.MOTOR_PWM_FREQ)
        SharedConstants.LEFT_MOTOR_PWM[0].start(0)
        GPIO.setup(SharedConstants.P_LEFT_BACKWARD, GPIO.OUT)
        SharedConstants.LEFT_MOTOR_PWM[1] = GPIO.PWM(SharedConstants.P_LEFT_BACKWARD, SharedConstants.MOTOR_PWM_FREQ)
        SharedConstants.LEFT_MOTOR_PWM[1].start(0)

        # Right motor
        GPIO.setup(SharedConstants.P_RIGHT_FORWARD, GPIO.OUT)
        SharedConstants.RIGHT_MOTOR_PWM[0] = GPIO.PWM(SharedConstants.P_RIGHT_FORWARD, SharedConstants.MOTOR_PWM_FREQ)
        SharedConstants.RIGHT_MOTOR_PWM[0].start(0)
        GPIO.setup(SharedConstants.P_RIGHT_BACKWARD, GPIO.OUT)
        SharedConstants.RIGHT_MOTOR_PWM[1] = GPIO.PWM(SharedConstants.P_RIGHT_BACKWARD, SharedConstants.MOTOR_PWM_FREQ)
        SharedConstants.RIGHT_MOTOR_PWM[1].start(0)

        # IR sensors
        GPIO.setup(SharedConstants.P_FRONT_LEFT, GPIO.IN)
        GPIO.setup(SharedConstants.P_FRONT_CENTER, GPIO.IN)
        GPIO.setup(SharedConstants.P_FRONT_RIGHT, GPIO.IN)
        GPIO.setup(SharedConstants.P_LINE_LEFT, GPIO.IN)
        GPIO.setup(SharedConstants.P_LINE_RIGHT, GPIO.IN)

        # Establish event recognition from battery monitor
        GPIO.setup(SharedConstants.P_BATTERY_MONITOR, GPIO.IN, GPIO.PUD_UP)
        GPIO.add_event_detect(SharedConstants.P_BATTERY_MONITOR, GPIO.RISING, _onBatteryDown)

        # I2C PWM chip for LEDs
        Tools.debug("Trying to detect PCA9685 PCM chip on I2C bus using bus number 1...")
        try:
            self.ledPWM = PWM(0x40, busnumber = 1, debug = False)
            self.ledPWM.setPWMFreq(SharedConstants.LED_PWM_FREQ)
            Tools.debug("PCA9685 PCM chip on I2C bus detected")
        except:
            Tools.debug("Failed, trying with bus number 0...")
            try:
                self.ledPWM = PWM(0x40, busnumber = 0, debug = False)
                self.ledPWM.setPWMFreq(SharedConstants.LED_PWM_FREQ)
                Tools.debug("PCA9685 PCM chip on I2C bus detected")
            except:
                print "Failed to detect PCA9685 PCM chip on I2C bus"
                sys.exit(1)

        # clear all LEDs
        for id in range(3):
            self.ledPWM.setPWM(3 * id, 0, 0)
            self.ledPWM.setPWM(3 * id + 1, 0, 0)
            self.ledPWM.setPWM(3 * id + 2, 0, 0)

        # I2C analog extender chip
        Tools.debug("Trying to detect PCF8591 I2C analog extender on I2C bus 1...")
        try:
            self.analogExtender = sgh_PCF8591P(1) # i2c at address 0x48
            Tools.debug("PCF8591 I2C analog extender on I2C bus # 1 detected")
        except:
            print "Failed, trying with bus number 0..."
            try:
                self.analogExtender = sgh_PCF8591P(0) # i2c at address 0x48
                print "PCF8591 I2C analog extender on I2C bus # 0 detected"
            except:
                print "Failed to detect PCF8591 I2C analog extender on I2C bus"
                sys.exit(1)

        Tools.debug("Trying to detect 7-segment display and clear it")
        addr = 0x20
        self._isDisplayAvailable = True
        self._bus = None
        try:
            if GPIO.RPI_REVISION > 1:
                self._bus = smbus.SMBus(1) # For revision 2 Raspberry Pi
            else:
                self._bus = smbus.SMBus(0) # For revision 1 Raspberry Pi
            Tools.debug("7-segment display found.")
        except:
            print "No 7-segment display found on this robot device."
            self._isDisplayAvailable = False

        # Clear display, if available
        if self._isDisplayAvailable:
            try:
                self._bus.write_byte_data(addr, 0x00, 0x00) # Set all of bank 0 to outputs
                self._bus.write_byte_data(addr, 0x01, 0x00) # Set all of bank 1 to outputs
                self._bus.write_byte_data(addr, 0x13, 0xff) # Set all of bank 1 to high (all digits off)
            except:
                print "No 7-segment display found on this robot device."
                self._isDisplayAvailable = False

        GPIO.setup(SharedConstants.P_BUTTON, GPIO.IN, GPIO.PUD_UP)
        # Establish event recognition from button event
        GPIO.add_event_detect(SharedConstants.P_BUTTON, GPIO.BOTH, _onButtonEvent)
        _isButtonEnabled = True
        Tools.debug("MyRobot instance created")
        MyRobot._myInstance = self

    def exit(self):
        """
        Cleans-up and releases all resources.
        """
        global _isButtonEnabled
        Tools.debug("Calling Robot.exit()")
        self.setButtonEnabled(False)

        # Stop motors
        SharedConstants.LEFT_MOTOR_PWM[0].ChangeDutyCycle(0)
        SharedConstants.LEFT_MOTOR_PWM[1].ChangeDutyCycle(0)
        SharedConstants.RIGHT_MOTOR_PWM[0].ChangeDutyCycle(0)
        SharedConstants.RIGHT_MOTOR_PWM[1].ChangeDutyCycle(0)

        # Stop button thread, if necessary
        if _buttonThread != None:
            _buttonThread.stop()

        # Stop display
        display = Display._myInstance
        if display != None:
            display.stopTicker()
            display.clear()

        Led.clearAll()
        Tools.delay(2000)  # avoid "sys.excepthook is missing"

    def isButtonDown(self):
        '''
        Checks if button is currently pressed.
        @return: True, if the button is actually pressed
        '''
        Tools.delay(1);
        return GPIO.input(SharedConstants.P_BUTTON) == GPIO.LOW

    def isButtonHit(self):
        '''
        Checks, if the button was ever hit or hit since the last invocation.
        @return: True, if the button was hit; otherwise False
        '''
        global _isBtnHit
        Tools.delay(1)
        hit = _isBtnHit
        _isBtnHit = False
        return hit

    def isEscapeHit(self):
        '''
        Same as isButtonHit() for compatibility with remote mode.
        '''
        return self.isButtonHit()

    def isEnterHit(self):
        '''
        Empty method for compatibility with remote mode.
        '''
        pass

    def isUpHit(self):
        '''
        Empty method for compatibility with remote mode.
        '''
        pass

    def isDownHit(self):
        '''
        Empty method for compatibility with remote mode.
        '''
        pass

    def isLeftHit(self):
        '''
        Empty method for compatibility with remote mode.
        '''
        pass

    def isRightHit(self):
        '''
        Empty method for compatibility with remote mode.
        '''
        pass

    def addButtonListener(self, listener):
        '''
        Registers a listener function to get notifications when the pushbutton is pressed or released.
        @param listener: the listener function (with boolean parameter isPressed) to register.
        '''
        global _buttonListener
        _buttonListener = listener

    def setButtonEnabled(self, enable):
        '''
        Enables/disables the push button. The button is enabled, when the Robot is created.
        @param enable: if True, the button is enabled; otherwise disabled
        '''
        Tools.debug("Calling setButtonEnabled() with enable = " + str(enable))
        global _isButtonEnabled
        _isButtonEnabled = enable

    def addBatteryMonitor(self, listener):
        '''
        There is a small processor on the PCB (an STM8S003F3P6) which handles the voltage monitoring,
        as well as trying to reduce the impact of direct light on the IR sensors.
        It has 2 threshold voltages: At about 6.5V (3 consecutive readings) it flashes the red LED and
        disables the motor drivers. At about 6.2V it turns the red LED on permanently and
        sends a signal on GPIO24 pin 18 to the Pi. The software on the Pi can monitor this and
        shut down gracefully if required. If the voltage goes back above 7.0V then the system resets
        to Green LED and all enabled.

        Registers a listener function to get notifications when battery voltage is getting low.
        @param listener: the listener function (with no parameter) to register
        '''
        batteryListener = listener

