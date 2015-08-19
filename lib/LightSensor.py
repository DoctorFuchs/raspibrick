# LightSensor.java

'''
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
    Class that represents an ultrasonic sensor.
    '''
    def __init__(self, id):
        '''
        Creates a light sensor instance with given id.
        IDs: 0: front left, 1: front right, 2: rear left, 3: rear right
        The following global constants are defined:
        LS_FRONT_LEFT = 0, LS_FRONT_RIGHT = 1, LS_REAR_LEFT = 2, LS_REAR_RIGHT = 3.
        @param id: the LightSensor identifier
        '''
        self.id = id
        Tools.debug("LightSensor instance with ID " + str(id) + " created")

    def getValue(self):
        '''
        Returns the current intensity value (0..255).
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
        return robot.analogExtender.readADC(nb)

    def _checkRobot(self):
        if RobotInstance.getRobot() == None:
            raise Exception("Create Robot instance first")


