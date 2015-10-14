# LightSensor.java

'''
Class that represents a light sensor.

 This software is part of the raspibrick module.
 It is Open Source Free Software, so you may
 - run the code for any purpose
 - study how the code works and adapt it to your needs
 - integrate all or parts of the code in your own programs
 - redistribute copies of the code777
 - improve the code and release your improvements to the public
 However the use of the code is entirely your responsibility.
 '''

from Tools import Tools
from RobotInstance import RobotInstance

class LightSensor():
    '''
    Class that represents an light sensor.
    '''
    def __init__(self, id, **kwargs):
        '''
        Creates a light sensor instance with given id.
        IDs: 0: front left, 1: front right, 2: rear left, 3: rear right
        The following global constants are defined:
        LS_FRONT_LEFT = 0, LS_FRONT_RIGHT = 1, LS_REAR_LEFT = 2, LS_REAR_RIGHT = 3.
        @param id: the LightSensor identifier
        '''
        self.id = id
        self.sensorState = "DARK"
        self.sensorType = "LightSensor"
        self.triggerLevel = 500
        self.brightCallback = None
        self.darkCallback = None
        self.isRegistered = False
        for key in kwargs:
            if key == "bright":
                self.brightCallback = kwargs[key]
            elif key == "dark":
                self.darkCallback = kwargs[key]
        robot = RobotInstance.getRobot()
        if robot == None:  # deferred registering, because Robot not yet created
            RobotInstance._sensorsToRegister.append(self)
        else:
            if self.brightCallback != None or self.darkCallback != None:
                robot.registerSensor(self)
        Tools.debug("LightSensor instance with ID " + str(id) + " created")

    def getValue(self):
        '''
        Returns the current intensity value (0..1000).
        @return: the measured light intensity
        @rtype: int
        '''
        self._checkRobot()
        Tools.delay(1)
        nb = self.id
        if nb == 0:
            nb = 1
        elif nb == 1:
            nb = 0
        robot = RobotInstance.getRobot()
        return int(robot.analogExtender.readADC(nb) / 255.0 * 1000 + 0.5)

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

    def onBright(self, v):
        if self.brightCallback != None:
            self.brightCallback(self.id, v)

    def onDark(self, v):
        if self.darkCallback != None:
            self.darkCallback(self.id, v)

    def _checkRobot(self):
        if RobotInstance.getRobot() == None:
            raise Exception("Create Robot instance first")


