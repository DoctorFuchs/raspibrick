# InfraredSensor.java

'''
Class that represents an infrared sensor.

 This software is part of the raspibrick module.
 It is Open Source Free Software, so you may
 - run the code for any purpose
 - study how the code works and adapt it to your needs
 - integrate all or parts of the code in your own programs
 - redistribute copies of the code
 - improve the code and release your improvements to the public
 However the use of the code is entirely your responsibility.
 '''

from .Tools import Tools
import RPi.GPIO as GPIO
from . import SharedConstants
from .RobotInstance import RobotInstance

class InfraredSensor():
    '''
    Class that represents an infrared sensor.
    '''
    def __init__(self, id, **kwargs):
        '''
        Creates an infrared sensor at given port.
        For the Pi2Go the following infrared sensors are used:
        id = 0: front center; id = 1: front left; id = 2: front right;
        id = 3: line left; id = 4: line right. The following global constants are defined:
        IR_CENTER = 0, IR_LEFT = 1, IR_RIGHT = 2, IR_LINE_LEFT = 3, IR_LINE_RIGHT = 4
        @param id: sensor identifier
        '''
        self.id = id
        self.sensorState = "PASSIVATED"
        self.sensorType = "InfraredSensor"
        self.activateCallback = None
        self.passivateCallback = None
        for key in kwargs:
            if key == "activated":
                self.activateCallback = kwargs[key]
            elif key == "passivated":
                self.passivateCallback = kwargs[key]
        robot = RobotInstance.getRobot()
        if robot == None:  # deferred registering, because Robot not yet created
            RobotInstance._sensorsToRegister.append(self)
        else:
            if self.activateCallback != None or self.passivateCallback != None:
                robot.registerSensor(self)
        Tools.debug("InfraredSensor instance with ID " + str(id) + " created")

    def getValue(self):
        '''
        Checks, if reflected light is detected.
        @return: 1, if the sensor detects reflected light; otherwise 0
        @rtype: int
        '''
        Tools.delay(1)
        self._checkRobot()
        if self.id == SharedConstants.IR_CENTER and \
                    GPIO.input(SharedConstants.P_FRONT_CENTER) == GPIO.LOW:
            return 1
        elif self.id == SharedConstants.IR_LEFT and \
                    GPIO.input(SharedConstants.P_FRONT_LEFT) == GPIO.LOW:
            return 1
        elif self.id == SharedConstants.IR_RIGHT and \
                    GPIO.input(SharedConstants.P_FRONT_RIGHT) == GPIO.LOW:
            return 1
        elif self.id == SharedConstants.IR_LINE_LEFT and \
                    GPIO.input(SharedConstants.P_LINE_LEFT) == GPIO.LOW:
            return 1
        elif self.id == SharedConstants.IR_LINE_RIGHT and \
                    GPIO.input(SharedConstants.P_LINE_RIGHT) == GPIO.LOW:
            return 1
        else:
            return 0

    def getSensorState(self):
        return self.sensorState

    def setSensorState(self, state):
        self.sensorState = state

    def getSensorType(self):
        return self.sensorType

    def onActivated(self):
        if self.activateCallback != None:
            self.activateCallback(self.id)

    def onPassivated(self):
        if self.passivateCallback != None:
            self.passivateCallback(self.id)

    def _checkRobot(self):
        if RobotInstance.getRobot() == None:
            raise Exception("Create Robot instance first")

