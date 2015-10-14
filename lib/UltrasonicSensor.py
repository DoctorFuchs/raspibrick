# UltrasonicSensor.java

'''
Class that represents an ultrasonic sensor.

 This software is part of the raspibrick module.
 It is Open Source Free Software, so you may
 - run the code for any purpose
 - study how the code works and adapt it to your needs
 - integrate all or parts of the code in your own programs
 - redistribute copies of the code777
 - improve the code and release your improvements to the public
 However the use of the code is entirely your responsibility.
 '''

import SharedConstants
from RobotInstance import RobotInstance
from Tools import Tools
import RPi.GPIO as GPIO
import time

class UltrasonicSensor():
    '''
    Class that represents an ultrasonic sensor.
    '''
    def __init__(self, **kwargs):
        '''
        Creates a sensor instance.
        '''
        self.sensorState = "FAR"
        self.sensorType = "UltrasonicSensor"
        self.triggerLevel = 20
        self.nearCallback = None
        self.farCallback = None
        for key in kwargs:
            if key == "near":
                self.nearCallback = kwargs[key]
            elif key == "far":
                self.farCallback = kwargs[key]
        robot = RobotInstance.getRobot()
        if robot == None:  # deferred registering, because Robot not yet created
            RobotInstance._sensorsToRegister.append(self)
        else:
            if self.nearCallback != None or self.farCallback != None:
                robot.registerSensor(self)
        Tools.debug("UltrasonicSensor instance created")

    def getValue(self):
        '''
        Returns the distance.
        @return: Distance from target in cm, or -1 if no object or error
        @rtype: float
        '''
        self._checkRobot()
        # Set pins as output and input
        GPIO.setup(SharedConstants.P_TRIG_ECHO, GPIO.OUT)
        GPIO.output(SharedConstants.P_TRIG_ECHO, GPIO.LOW)

        # Allow module to settle
        time.sleep(0.1)

        # Send max 10 us trigger pulse
        GPIO.output(SharedConstants.P_TRIG_ECHO, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(SharedConstants.P_TRIG_ECHO, GPIO.LOW)

        # Prepare for echo
        GPIO.setup(SharedConstants.P_TRIG_ECHO, GPIO.IN)

        # Determine echo pulse length
        start = time.time()
        count = start

        # Wait max 1 s for HIGH signal
        while GPIO.input(SharedConstants.P_TRIG_ECHO) == GPIO.LOW and count - start < 1:
            count = time.time()
        if count - start >= 1:
            Tools.debug("Timeout while waiting for echo going HIGH")
            return -1 # error

        # Wait  for LOW signal
        while GPIO.input(SharedConstants.P_TRIG_ECHO) == GPIO.HIGH:
            continue
        stop = time.time()

        # Calculate pulse length
        elapsed = stop - start

        # Distance = speed_of_sound * elapsed / 2
        distance =  34300 * elapsed / 2.0
        # round to 2 decimals
        distance = int(distance * 100 + 0.5) / 100.0
        return distance

    def getDistance(self):
        '''
        Returns the distance.
        @return: Distance from target in cm formatted to two decimals, or -1 if no object or error
        @rtype: str
        '''
        return format(self.getValue(), ".2f")

    def getTriggerLevel(self):
        return self.triggerLevel

    def setTriggerLevel(self, level):
        self.triggerLevel = level

    def getSensorState(self):
        return self.sensorState

    def setSensorState(self, state):
        self.sensorState = state

    def getSensorType(self):
        return self.sensorType

    def onNear(self, v):
        if self.nearCallback != None:
            self.nearCallback(v)

    def onFar(self, v):
        if self.farCallback != None:
            self.farCallback(v)

    def _checkRobot(self):
        if RobotInstance.getRobot() == None:
            raise Exception("Create Robot instance first")

