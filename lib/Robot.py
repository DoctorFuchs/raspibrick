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
from smbus import SMBus
import RPi.GPIO as GPIO
import os, sys
import time
from Tools import Tools
import SharedConstants
from Display import Display
from DgTell import DgTell
from DgTell1 import DgTell1
from Disp4tronix import Disp4tronix
from SensorThread import SensorThread
from Led import Led
from PCA9685 import PWM
from threading import Thread
from subprocess import Popen, PIPE
import re
import smbus
import pygame

# --------------------------- class ButtonThread ------------
class ButtonThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.isRunning = False

    def run(self):
        Tools.debug("===>ButtonThread started")
        self.isRunning = True
        startTime = time.time()
        while self.isRunning and (time.time() - startTime < SharedConstants.BUTTON_LONGPRESS_DURATION):
            time.sleep(0.1)
        if self.isRunning:
            if _buttonListener != None:
                _buttonListener(SharedConstants.BUTTON_LONGPRESSED)
        Tools.debug("===>ButtonThread terminated")

    def stop(self):
        self.isRunning = False

# --------------------------- class ClickThread -------------
class ClickThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.start()

    def run(self):
        Tools.debug("===>ClickThread started")
        global _clickThread
        self.isRunning = True
        startTime = time.time()
        while self.isRunning and (time.time() - startTime < SharedConstants.BUTTON_DOUBLECLICK_TIME):
            time.sleep(0.1)
        if _clickCount == 1 and not _isLongPressEvent:
            if _xButtonListener != None:
                _xButtonListener(SharedConstants.BUTTON_CLICKED)
        _clickThread = None
        Tools.debug("===>ClickThread terminated")

    def stop(self):
        self.isRunning = False


# --------------------------- Global functions ------------------------
def _onXButtonEvent(event):
    global _clickThread, _clickCount, _isLongPressEvent
    if event == SharedConstants.BUTTON_PRESSED:
        if _xButtonListener != None:
            _xButtonListener(SharedConstants.BUTTON_PRESSED)
        _isLongPressEvent = False
        if _clickThread == None:
            _clickCount = 0
            _clickThread = ClickThread()

    elif event == SharedConstants.BUTTON_RELEASED:
        if _xButtonListener != None:
            _xButtonListener(SharedConstants.BUTTON_RELEASED)
        if _isLongPressEvent:
            _clickThread.stop()
            _clickThread = None
            return
        _clickCount += 1
        if _clickThread != None:
            if _clickCount == 2:
                _clickThread.stop()
                _clickThread = None
                if _xButtonListener != None:
                    _xButtonListener(SharedConstants.BUTTON_DOUBLECLICKED)
        else:
                if _xButtonListener != None:
                    _xButtonListener(SharedConstants.BUTTON_CLICKED)

    elif event == SharedConstants.BUTTON_LONGPRESSED:
        _isLongPressEvent = True
        if _xButtonListener != None:
            _xButtonListener(SharedConstants.BUTTON_LONGPRESSED)

def _onButtonEvent(channel):
    # switch may bounce: down-up-up, down-up-down, down-down-up etc. in fast sequence
    if not _isButtonEnabled:
        Tools.debug("Button event detected, but button disabled")
        return
    global _isBtnHit, _buttonThread
    try:
        if GPIO.input(SharedConstants.P_BUTTON) == GPIO.LOW:
            if _buttonThread == None: # down-down is suppressed
                Tools.debug("ButtonDown event on channel " + str(channel))
                _isBtnHit = True
                _buttonThread = ButtonThread()
                _buttonThread.start()
                if _buttonListener != None:
                    _buttonListener(SharedConstants.BUTTON_PRESSED)
        else:
            if _buttonThread != None:  # up-up is suppressed
                Tools.debug("ButtonUp event on channel " + str(channel))
                _buttonThread.stop()
                _buttonThread.join(200) # wait until finished
                _buttonThread = None
                if _buttonListener != None:
                    _buttonListener(SharedConstants.BUTTON_RELEASED)
    except:  # NoneType error when program is already terminated
        pass

def _onBatteryDown(channel):
    Tools.debug("onBatteryDown event on channel " + str(channel))
    if _batteryListener != None:
        _batteryListener()

# --------------------------- Global variables ------------------------
_buttonThread = None
_clickThread = None
_doubleClickTime = SharedConstants.BUTTON_DOUBLECLICK_TIME
_buttonListener = None
_xButtonListener = None
_batteryListener = None
_isBtnHit = False
_isButtonEnabled = False

# ------------------------   Class Robot   -------------------------------------------------
class Robot(object):
    '''
    Class that creates or returns a single MyRobot instance.
    Signature for the butten event callback: buttonEvent(int).
    (BUTTON_PRESSED, BUTTON_RELEASED, BUTTON_LONGPRESSED defined in ShareConstants.)
    @param ipAddress the IP address (default: None for autonomous mode)
    @param buttonEvent the callback function for pushbutton events (default: None)
    '''
    def __new__(cls, ipAddress = "", buttonEvent = None):
        global _isBtnHit
        if RobotInstance.getRobot() == None:
            r = MyRobot(ipAddress, buttonEvent)
            r.isEscapeHit()  # Dummy to clear button hit flag
            RobotInstance.setRobot(r)
            for sensor in RobotInstance._sensorsToRegister:
                r.registerSensor(sensor)
            return r
        else:
            r = RobotInstance.getRobot()
            r.isEscapeHit()  # Dummy to clear button hit flag
            return RobotInstance.getRobot()

# ------------------------   Class MyRobot   -----------------------------------------------
class MyRobot(object):
    '''
    Singleton class that represents a robot.
    Signature for the butten event callback: buttonEvent(int).
    (BUTTON_PRESSED, BUTTON_RELEASED, BUTTON_LONGPRESSED defined in ShareConstants.)
    @param ipAddress the IP address (default: None for autonomous mode)
    @param buttonEvent the callback function for pushbutton events (default: None)
    '''
    _myInstance = None
    def __init__(self, ipAddress = "", buttonEvent = None):
        '''
        Creates an instance of MyRobot and initalizes the GPIO.
        '''
        if MyRobot._myInstance != None:
            raise Exception("Only one instance of MyRobot allowed")
        global _isButtonEnabled, _buttonListener

        _buttonListener = buttonEvent

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
        GPIO.setup(SharedConstants.P_FRONT_LEFT, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(SharedConstants.P_FRONT_CENTER, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(SharedConstants.P_FRONT_RIGHT, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(SharedConstants.P_LINE_LEFT, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(SharedConstants.P_LINE_RIGHT, GPIO.IN, GPIO.PUD_UP)

        # Establish event recognition from battery monitor
        GPIO.setup(SharedConstants.P_BATTERY_MONITOR, GPIO.IN, GPIO.PUD_UP)
        GPIO.add_event_detect(SharedConstants.P_BATTERY_MONITOR, GPIO.RISING, _onBatteryDown)

        Tools.debug("Trying to detect I2C bus")
        isSMBusAvailable = True
        self._bus = None
        try:
            if GPIO.RPI_REVISION > 1:
                self._bus = smbus.SMBus(1) # For revision 2 Raspberry Pi
                Tools.debug("Found SMBus for revision 2")
            else:
                self._bus = smbus.SMBus(0) # For revision 1 Raspberry Pi
                Tools.debug("Found SMBus for revision 1")
        except:
            print "No SMBus found on this robot device."
            isSMBusAvailable = False

        # I2C PWM chip PCM9685 for LEDs and servos
        if isSMBusAvailable:
            self.pwm = PWM(self._bus, SharedConstants.PWM_I2C_ADDRESS)
            self.pwm.setFreq(SharedConstants.PWM_FREQ)
            # clear all LEDs
            for id in range(3):
                self.pwm.setDuty(3 * id, 0)
                self.pwm.setDuty(3 * id + 1, 0)
                self.pwm.setDuty(3 * id + 2, 0)

        # I2C analog extender chip
        if isSMBusAvailable:
            Tools.debug("Trying to detect PCF8591P I2C expander")
            channel = 0
            try:
                self._bus.write_byte(SharedConstants.ADC_I2C_ADDRESS, channel)
                self._bus.read_byte(SharedConstants.ADC_I2C_ADDRESS) # ignore reply
                data = self._bus.read_byte(SharedConstants.ADC_I2C_ADDRESS)
                Tools.debug("Found PCF8591P I2C expander")
            except:
                Tools.debug("PCF8591P I2C expander not found")

        Tools.debug("Trying to detect 7-segment display")
        if isSMBusAvailable:
            self.displayType = "none"
            try:
                addr = 0x20
                rc = self._bus.read_byte_data(addr, 0)
                if rc != 0xA0:   # returns 255 for 4tronix
                    raise Exception()
                Tools.delay(100)
                self.displayType = "didel1"
            except:
                Tools.debug("'didel1' display not found")
            if self.displayType == "none":
                try:
                    addr = 0x20
                    self._bus.write_byte_data(addr, 0x00, 0x00) # Set all of bank 0 to outputs
                    Tools.delay(100)
                    self.displayType = "4tronix"
                except:
                    Tools.debug("'4tronix' display not found")
                if self.displayType == "none":
                    try:
                        addr = 0x24
                        data = [0] * 4
                        self._bus.write_i2c_block_data(addr, data[0], data[1:])  # trying to clear display
                        self.displayType = "didel"
                    except:
                        Tools.debug("'didel' display not found")

            Tools.debug("Display type '" + self.displayType + "'")

            # Initializing (clear) display, if available
            if self.displayType == "4tronix":
                Disp4tronix().clear()
            if self.displayType == "didel":
                DgTell().clear()
            if self.displayType == "didel1":
                DgTell1().clear()

        GPIO.setup(SharedConstants.P_BUTTON, GPIO.IN, GPIO.PUD_UP)
        # Establish event recognition from button event
        GPIO.add_event_detect(SharedConstants.P_BUTTON, GPIO.BOTH, _onButtonEvent)
        _isButtonEnabled = True
        Tools.debug("MyRobot instance created. Lib Version: " + SharedConstants.VERSION)
        self.sensorThread = None
        MyRobot._myInstance = self

    def registerSensor(self, sensor):
        if self.sensorThread == None:
            self.sensorThread = SensorThread()
            self.sensorThread.start()
        self.sensorThread.add(sensor)


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
        MyRobot.closeSound()

        if self.sensorThread != None:
            self.sensorThread.stop()
            self.sensorThread.join(2000)

        GPIO.cleanup()
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

    def addButtonListener(self, listener, enableClick = False,
                          doubleClickTime = SharedConstants.BUTTON_DOUBLECLICK_TIME):
        '''
        Registers a listener function to get notifications when the pushbutton is pressed, released or long pressed.
        If enableClick = True, in addition click and double-click events are reported. The click event not immediately
        reported, but only if within the doubleClickTime no other click is gererated.
        The value are defined as ShareConstants.BUTTON_PRESSED, ShareConstants.BUTTON_LONGPRESSED, ShareConstants.BUTTON_RELEASED,
        ShareConstants.BUTTON_CLICKED, ShareConstants.BUTTON_DOUBLECLICKED.
        With enableClick = False and the button is long pressed and released the sequence is: BUTTON_PRESSED, BUTTON_LONGPRESSED, BUTTON_RELEASED.
        With enableClick = True the sequences are the following:
        click: BUTTON_PRESSED, BUTTON_RELEASED, BUTTON_CLICKED
        double-click: BUTTON_PRESSED, BUTTON_RELEASED, BUTTON_PRESSED, BUTTON_RELEASED, BUTTON_DOUBLECLICKED
        long pressed: BUTTON_PRESSED, BUTTON_LONGPRESSED,  BUTTON_RELEASED
        @param listener: the listener function (with boolean parameter event) to register.
        @param enableClick: if True, the click/double-click is also registered (default: False)
        @param doubleClickTime: the time (in seconds) to wait for a double click (default: set in SharedContants)
        '''
        if enableClick:
            global _xButtonListener, _doubleClickTime
            _doubleClickTime = doubleClickTime
            self.addButtonListener(_onXButtonEvent)
            _xButtonListener = listener
        else:
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


# ---------------------------------------------- static methods -----------------------------------
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
        @param volume: the sound volume (0..100)
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

    @staticmethod
    def initSound(soundFile, volume):
        '''
        Prepares the given wav or mp3 sound file for playing with given volume (0..100). The sound
        sound channel is opened and a background noise is emitted.
        @param soundFile: the sound file in the local file system
        @volume: the sound volume (0..100)
        @returns: True, if successful; False if the sound system is not available or the sound file
        cannot be loaded
        '''
        try:
            pygame.mixer.init()
        except:
            # print "Error while initializing sound system"
            return False
        try:
            pygame.mixer.music.load(soundFile)
        except:
            pygame.mixer.quit()
            # print "Error while loading sound file", soundFile
            return False
        try:
            pygame.mixer.music.set_volume(volume / 100.0)
        except:
            return False
        return True

    @staticmethod
    def closeSound():
        '''
        Stops any playing sound and closes the sound channel.
        '''
        try:
            pygame.mixer.stop()
            pygame.mixer.quit()
        except:
            pass

    @staticmethod
    def playSound():
        '''
        Starts playing.
        '''
        try:
            pygame.mixer.music.play()
        except:
            pass

    @staticmethod
    def fadeoutSound(time):
        '''
        Decreases the volume slowly and stops playing.
        @param time: the fade out time in ms
        '''
        try:
            pygame.mixer.music.fadeout(time)
        except:
            pass

    @staticmethod
    def setSoundVolume(volume):
        '''
        Sets the volume while the sound is playing.
        @param volume: the sound volume (0..100)
        '''
        try:
            pygame.mixer.music.set_volume(volume / 100.0)
        except:
            pass

    @staticmethod
    def stopSound():
        '''
        Stops playing sound.
        '''
        try:
            pygame.mixer.music.stop()
        except:
            pass

    @staticmethod
    def pauseSound():
        '''
        Temporarily stops playing at current position.
        '''
        try:
            pygame.mixer.music.pause()
        except:
            pass

    @staticmethod
    def resumeSound():
        '''
        Resumes playing from stop position.
        '''
        try:
            pygame.mixer.music.unpause()
        except:
            pass

    @staticmethod
    def rewindSound():
        '''
        Resumes playing from the beginning.
        '''
        try:
            pygame.mixer.music.rewind()
        except:
            pass

    @staticmethod
    def isSoundPlaying():
        '''
        @return: True, if the sound is playing; otherwise False
        '''
        try:
            return pygame.mixer.music.get_busy()
        except:
            return False

