# Led.java
# Remote mode

'''
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
from Tools import Tools

class Led():
    '''
    Class that represents a LED pair.
    '''
    def __init__(self, id):
        '''
        Creates a Led instance with given ID.
        IDs of the double LEDs: 0: front, 1: left side , 2: rear, 3: right side.
        The following global constants are defined:
        LED_FRONT = 0, LED_LEFT = 1, LED_REAR = 2, RED_RIGHT = 3.
        @param id: the LED identifier
        '''
        self.id = id
        self.device = "led" + str(id)
        robot = RobotInstance.getRobot()
        if robot == None:  # deferred registering, because Robot not yet created
            RobotInstance._partsToRegister.append(self)
        else:
            self._setup(robot)

    def _setup(self, robot):
        robot.sendCommand(self.device + ".create")
        self.robot = robot

    def setColor(self, *args):
        '''
        Sets the RGB color value of the two LEDs with current ID.
        @param args list of [red, green, blue] RGB color components 0..255
            or three color integers 0..255
        '''
        self._checkRobot()
        if len(args) == 1 and type(args[0]) == list:
            red = args[0][0]
            green = args[0][1]
            blue = args[0][2]
        elif len(args) == 3:
            red = args[0]
            green = args[1]
            blue = args[2]
        else:
            raise ValueError("Illegal param in setColor()")
        self.robot.sendCommand(self.device + ".setColor." +
            str(red) + "." + str(green) + "." + str(blue))

    @staticmethod
    def setColorAll(*args):
        '''
        Sets the RGB color of all 4 LED pairs.
        @param color list of [red, green, blue] RGB color components 0..255
         or three color integers 0..255
        '''
        if RobotInstance.getRobot() == None:
            raise Exception("Create Robot instance first")
        if len(args) == 1 and type(args[0]) == list:
            red = args[0][0]
            green = args[0][1]
            blue = args[0][2]
        elif len(args) == 3:
            red = args[0]
            green = args[1]
            blue = args[2]
        else:
            raise ValueError("Illegal param in setColor()")
        RobotInstance.getRobot().sendCommand("led.setColorAll." +
            str(red) + "." + str(green) + "." + str(blue))

    @staticmethod
    def clearAll():
        '''
        Turns off all 4 LED pairs.
        '''
        if RobotInstance.getRobot() == None:
            raise Exception("Create Robot instance first")
        RobotInstance.getRobot().sendCommand("led.clearAll")

    def _checkRobot(self):
        if RobotInstance.getRobot() == None:
            raise Exception("Create Robot instance first")

