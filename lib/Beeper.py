# Beeper.py

'''
Class that represents an active buzzer on some GPIO port.

 
 This software is part of the raspibrick module.
 It is Open Source Free Software, so you may
 - run the code for any purpose
 - study how the code works and adapt it to your needs
 - integrate all or parts of the code in your own programs
 - redistribute copies of the code777
 - improve the code and release your improvements to the public
 However the use of the code is entirely your responsibility.
'''

from . import SharedConstants
from .RobotInstance import RobotInstance
from .Tools import Tools
from threading import Thread
import RPi.GPIO as GPIO
import time


class Beeper():
    '''
    Abstraction of the beeper attached to given port (and ground).
    @param port: the GPIO port number (default: 40)
    '''
    def __init__(self, pin = 40):
        self._checkRobot()
        self.robot = RobotInstance.getRobot()
        self._pin = pin
        self._beeperThread = None
        Tools.debug("Beeper instance created with beeper at pin: " + str(pin))
        GPIO.setup(pin, GPIO.OUT)
        self.turnOff()
    
    def turnOn(self):
        '''
        Turns the beeper on.
        '''
        Tools.debug("Beeper turned on")
        GPIO.output(self._pin, GPIO.HIGH)

    def turnOff(self):
        '''
        Turns the beeper off.
        '''
        Tools.debug("Beeper turned off")
        GPIO.output(self._pin, GPIO.LOW)

    def beep(self, count = 1):
        '''
        Emits a short beep the given number of times. Blocking until the beeps are played.
        @param count: the number of beeps
        '''
        self.start(60, 120, count, True)
    
    def start(self, onTime, offTime, count = 0, blocking = False):
        '''
        Starts beeping. The beeping period is offTime + onTime. 
        May be stopped by calling stop(). If blocking is False, the
        function returns immediately while the blinking goes on. The blinking is stopped by setColor().
        @param onTime: the time in ms in on state
        @param offTime: the time in ms in off state
        @param count: total number of on states; 0 for endlessly (default)
        @param blocking: if True, the method blocks until the beeper has finished; otherwise
         it returns immediately (default: False)
        '''
        Tools.debug("Starting beeper with params onTime = " +  str(onTime) + 
            " offTime = " +  str(offTime) + 
            " count = " + str(count) + 
           " blocking = " + str(blocking))
        if self._beeperThread != None:
            self.stop()
        self._beeperThread = BeeperThread(self, onTime, offTime, count)
        if blocking:
            while self.isBeeping():
                continue

    def setOffTime(self, offTime):
        '''
        Sets the time the speaker is off.
        @param offTime: the offTime in ms
        '''
        if self._beeperThread != None:
            self._beeperThread._offTime = offTime

    def setOnTime(self, onTime):
        '''
        Sets the time the speaker is on.
        @param onTime: the onTime in ms
        '''
        if self._beeperThread != None:
            self._beeperThread._onTime = onTime

    def setOnOffTime(self, onTime, offTime):
        '''
        Sets the time the speaker is on and off.
        @param onTime: the onTime in ms
        @param offTime: the offTime in ms
        '''
        if self._beeperThread != None:
            self._beeperThread._onTime = onTime
            self._beeperThread._offTime = offTime
       
    def stop(self):
        '''
        Stops beeping.
        '''
        if self._beeperThread != None:
            self._beeperThread.stop()

    def isBeeping(self):
        '''
        @return: True, if the beeper is active; otherwise False
        '''
        time.sleep(0.001)
        return self._beeperThread != None
    
      
    def _checkRobot(self):
        if RobotInstance.getRobot() == None:
            raise Exception("Create Robot instance first")




# ------------------- class BeeperThread ----------------------
class BeeperThread(Thread):
    def __init__(self, beeper, onTime, offTime, count):
        Thread.__init__(self)
        self._beeper = beeper
        self._onTime = onTime
        self._offTime = offTime
        self._count = count
        self._isAlive = True
        self.start()

    def run(self):
        Tools.debug("Beeper thread started")
        nb = 0
        self._isRunning = True
        while self._isRunning:
            if self._onTime <= 0:
                self._beeper.turnOff()
                time.sleep(0.01)
            else:
                self._beeper.turnOn()
                startTime = time.time()
                while time.time() - startTime < self._onTime / 1000 and self._isRunning:
                    time.sleep(0.001)
                if not self._isRunning:
                    break
    
                self._beeper.turnOff()
                startTime = time.time()
                while time.time() - startTime < self._offTime / 1000 and self._isRunning:
                    time.sleep(0.001)
            if not self._isRunning:
                break

            nb += 1
            if nb == self._count:
                self._isRunning = False
        self._beeper.turnOff()
        self._beeper._beeperThread = None
        self._isAlive = False
        Tools.debug("Beeper thread finished")

    def stop(self):
        self._isRunning = False
        while self._isAlive: # Wait until thread is finished
            continue
